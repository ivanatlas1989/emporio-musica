
import os
import re
import math
import json
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from google import genai
from google.genai import types

from ler_politicas import chunks
from consultar_produtos import consultar_produto
from consultar_pedidos import consultar_pedido_autorizado


# =====================================
# 1. CONEXAO COM GEMINI
# =====================================

load_dotenv()

chave = os.getenv("GEMINI_API_KEY")

if not chave:
    raise ValueError("Chave de API não encontrada!")

cliente = genai.Client(
    api_key=chave,
    http_options=types.HttpOptions(timeout=30000)
)


# =====================================
# 2. SIMILARIDADE DE COSSENO
# =====================================

def similaridade(vetor_a, vetor_b):
    produto = sum(a * b for a, b in zip(vetor_a, vetor_b))

    tamanho_a = math.sqrt(sum(a * a for a in vetor_a))
    tamanho_b = math.sqrt(sum(b * b for b in vetor_b))

    if tamanho_a == 0 or tamanho_b == 0:
        return 0

    return produto / (tamanho_a * tamanho_b)


# =====================================
# 3. EMBEDDINGS DO PDF
# =====================================

embeddings = []

for chunk in chunks:
    resposta = cliente.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )

    embeddings.append(resposta.embeddings[0].values)

print("[RAG] Embeddings carregados:", len(embeddings))


# =====================================
# 4. CONSULTA DAS POLITICAS
# =====================================

def consultar_politica(pergunta: str) -> dict:
    """Busca no manual as politicas relevantes para uma pergunta."""

    print("\n[RAG] Consultando políticas:", pergunta)

    resposta = cliente.models.embed_content(
        model="gemini-embedding-001",
        contents=pergunta
    )

    embedding_pergunta = resposta.embeddings[0].values

    resultados = []

    for indice, embedding in enumerate(embeddings):
        pontuacao = similaridade(
            embedding_pergunta,
            embedding
        )
        resultados.append((indice, pontuacao))

    resultados.sort(
        key=lambda item: item[1],
        reverse=True
    )

    melhores = resultados[:2]
    trechos = []

    for indice, pontuacao in melhores:
        print(
            f"[RAG] Chunk {indice + 1} | "
            f"Similaridade: {pontuacao:.4f}"
        )

        trechos.append(chunks[indice])

    return {
        "trechos": trechos,
        "fonte": "Manual de Políticas e Procedimentos"
    }


# =====================================
# 5. CONTEXTO DE PRODUTOS
# =====================================

contexto_produto = {
    "nome": "",
    "preco_referencia": None
}

instrumentos = [
    "violão", "violao", "guitarra", "baixo",
    "teclado", "bateria", "piano", "ukulele",
    "saxofone", "flauta", "violino",
    "yamaha", "giannini"
]


def extrair_preco(pergunta):
    """Identifica limites de preco mencionados pelo cliente."""

    padrao = r"(?:R\$\s*|até\s+)([\d.]+(?:,\d{1,2})?)"

    encontrado = re.search(
        padrao,
        pergunta,
        flags=re.IGNORECASE
    )

    if not encontrado:
        return None

    valor = encontrado.group(1)
    valor = valor.replace(".", "").replace(",", ".")

    return float(valor)


def identificar_produto(pergunta):
    """Identifica o instrumento ou modelo mencionado."""

    texto = pergunta.lower()

    for instrumento in instrumentos:
        if instrumento in texto:
            return instrumento

    return ""


def precisa_consultar_catalogo(pergunta):
    """Decide se esta mensagem precisa de dados do CSV."""

    texto = pergunta.lower()

    nome = identificar_produto(pergunta)

    if nome:
        return True

    palavras_comerciais = [
        "estoque", "disponível", "disponibilidade",
        "quanto custa", "preço", "valor",
        "mais barato", "mais cara",
        "mais barato?", "modelos", "catálogo",
        "até r$", "tem algum", "tem outro"
    ]

    if any(palavra in texto for palavra in palavras_comerciais):
        return True

    # Continuidade da busca anterior
    if contexto_produto["nome"]:
        continuacoes = [
            "e até", "até r$", "até ",
            "e por", "mais barato",
            "mais barato?", "outro modelo",
            "tem outro", "e esse", "e aquele"
        ]

        if any(texto.startswith(p) for p in continuacoes):
            return True

    return False


def preco_numerico(produto):
    return float(
        str(produto["preco"]).replace(",", ".")
    )


def consultar_catalogo_obrigatoriamente(pergunta):
    """Executa a busca real antes de o Gemini responder."""

    nome = identificar_produto(pergunta)

    if not nome:
        nome = contexto_produto["nome"]

    preco_maximo = extrair_preco(pergunta)

    texto = pergunta.lower()

    if "mais barato" in texto and preco_maximo is None:
        referencia = contexto_produto["preco_referencia"]

        if referencia is not None:
            preco_maximo = round(referencia - 0.01, 2)

    print("\n[CATALOGO] Consulta obrigatória")
    print("[CATALOGO] Nome:", nome or "Todos")
    print("[CATALOGO] Preço máximo:", preco_maximo)

    resultado = consultar_produto(
        nome=nome,
        preco_maximo=preco_maximo
    )

    print("[CATALOGO] Resultado:", resultado)

    if nome:
        contexto_produto["nome"] = nome

    produtos = resultado.get("produtos", [])

    if produtos:
        contexto_produto["preco_referencia"] = (
            preco_numerico(produtos[0])
        )

    return resultado


# =====================================
# 6. INSTRUCOES DO AGENTE
# =====================================

hoje = datetime.now(
    ZoneInfo("America/Sao_Paulo")
).strftime("%d/%m/%Y")
cliente_logado = {
    "customer_id": "2",
    "autenticado": True
}

def consultar_meu_pedido(numero_pedido: str) -> dict:
    return consultar_pedido_autorizado(
        numero_pedido,
        cliente_logado
    )

configuracao = types.GenerateContentConfig(
    system_instruction=f"""
    Você é o assistente virtual da Empório da Música,
    uma loja de instrumentos musicais em Campo Grande/MS.

    A data atual é {hoje}.

    Responda em português brasileiro, com cordialidade.

    REGRAS DE PRODUTOS:
    O Python consulta o catálogo antes de enviar
    informações comerciais para você.

    Quando receber um resultado do catálogo,
    use exclusivamente os dados recebidos.

    Nunca invente produtos, preços ou quantidades.
    Nunca afirme que consultou o catálogo sem evidência.
    Nunca simule erros técnicos.
    Nunca invente previsão de reposição.
    Nunca apresente textos como [Lista de produtos].
    Para consultar pedidos, use consultar_meu_pedido.
    Nunca revele dados de pedidos sem autorização.
    Se a ferramenta negar acesso, informe isso ao cliente.

    Se o resultado estiver vazio, informe que
    nenhum produto corresponde à busca.

    Lembre-se do instrumento mencionado anteriormente
    quando o cliente fizer perguntas de continuidade.

    POLITICAS:
    Use consultar_politica para horários,
    pagamentos, trocas, fretes, garantias e promoções.

    Nunca invente políticas.

    DEVOLUCOES:
    O prazo de arrependimento em compras online
    começa na data de recebimento, não na compra.

    Não presuma que uma compra foi online ou presencial.
    Se necessário, pergunte ao cliente.

    Nunca afirme que um prazo expirou sem informações
    suficientes. Não invente datas.

    Quando encontrar informações contraditórias,
    oriente o cliente a confirmar com a loja.

    Seja claro, objetivo e natural.
    """,
    tools=[consultar_politica, consultar_meu_pedido]
)


# =====================================
# 7. MEMORIA DE CONVERSA
# =====================================

chat = cliente.chats.create(
    model="gemini-3.1-flash-lite",
    config=configuracao
)


# =====================================
# 8. ATENDIMENTO
# =====================================

print("\nEmpório da Música - Atendimento virtual")
print("Digite 'sair' para encerrar.")

while True:
    pergunta = input("\nVocê: ").strip()

    if pergunta.lower() == "sair":
        break

    if not pergunta:
        print("Digite uma mensagem.")
        continue

    try:
        if precisa_consultar_catalogo(pergunta):

            resultado_catalogo = (
                consultar_catalogo_obrigatoriamente(pergunta)
            )

            # O Python ja fez a consulta real.
            # O Gemini recebe os dados consultados.

            mensagem = (
                f"Mensagem original do cliente: {pergunta}\n\n"
                "Resultado REAL da consulta ao catálogo CSV:\n"
                f"{json.dumps(resultado_catalogo, ensure_ascii=False)}\n\n"
                "Responda somente com os dados disponíveis. "
                "Não invente produtos, preços ou estoque."
            )

            resposta = chat.send_message(mensagem)

            # Impede a apresentação de produtos inventados
            # quando a busca retornou zero resultados.

            if not resultado_catalogo.get("produtos"):
                resposta_final = (
                    "Não encontrei produtos que atendam "
                    "aos critérios dessa busca no catálogo. "
                    "Podemos tentar outro modelo ou valor."
                )
            else:
                resposta_final = resposta.text

        else:
            resposta = chat.send_message(pergunta)
            resposta_final = resposta.text

        print("\nAtendente:", resposta_final)

    except Exception as erro:
        print("\n[ERRO REAL]:", erro)
        print(
            "\nAtendente: Não consegui concluir a consulta "
            "agora. Por favor, tente novamente."
        )
