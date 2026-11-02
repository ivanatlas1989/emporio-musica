import re
import pymupdf

documento = pymupdf.open("políticas_da_loja.pdf")

texto = ""

for pagina in documento:
    conteudo = pagina.get_text()

    conteudo = conteudo.replace(
        "Empório da Música Manual de Políticas e Procedimentos", ""
    )

    conteudo = re.sub(r"Página \d+", "", conteudo)

    texto += conteudo + "\n"

documento.close()

inicio = texto.index("EMPÓRIO DA MÚSICA")
fim = texto.index("3. Formas de Pagamento")

chunk_1 = texto[inicio:fim]
#print(chunk_1)

inicio = texto.index("3. Formas de Pagamento")
fim = texto.index("4. Política de Trocas e Devoluções")

chunk_2 = texto[inicio:fim]

#print("\n======CHUNK2=====")
#print(chunk_2)

inicio = texto.index("4. Política de Trocas e Devoluções")
fim = texto.index("5. Política de Frete e Entregas")

chunk_3 = texto[inicio:fim]
#print("\n======CHUNK3=====")
#print(chunk_3)

inicio = texto.index("5. Política de Frete e Entregas")
fim = texto.index("6. Promoções e Descontos")

chunk_4 = texto[inicio:fim]
#print("\n======CHUNK4=====")
#print(chunk_4)

inicio = texto.index("6. Promoções e Descontos")
fim = texto.index("7. Atendimento via WhatsApp")

chunk_5 = texto[inicio:fim]

#print("\n======CHUNK5=====")
#print(chunk_5)

inicio = texto.index("7. Atendimento via WhatsApp")
fim = texto.index("8. Garantia")

chunk_6 = texto[inicio:fim]

#print("\n======CHUNK6=====")
#print(chunk_6)

inicio = texto.index("8. Garantia")
fim = texto.index("9. Privacidade e Proteção de Dados")

chunk_7 = texto[inicio:fim]
#print("\n======CHUNK7=====")
#print(chunk_7)

inicio = texto.index("9. Privacidade e Proteção de Dados")

chunk_8 = texto[inicio:]
#print("\n======CHUNK8=====")
#print(chunk_8)

chunks = [
chunk_1,
chunk_2,
chunk_3,
chunk_4,
chunk_5,
chunk_6,
chunk_7,
chunk_8
]
#print("Total Chunks:", len(chunks))