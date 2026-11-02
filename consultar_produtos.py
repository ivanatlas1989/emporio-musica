import csv
from pathlib import Path
ultima_consulta = {
    "realizada": False,
    "resultados": []
}

def carregar_categorias():
    caminho = Path(__file__).parent / "categories.csv"

    with open(caminho, "r", encoding="utf-8-sig") as arquivo:
        categorias = csv.DictReader(arquivo, delimiter=",")

        return {
            categoria["name"].lower(): categoria["category_id"]
            for categoria in categorias
        }

def consultar_produto(
    nome: str = "",
    preco_maximo: float | None = None
) -> dict:
    """Consulta instrumentos por nome e preço máximo."""

    print(f"[DEBUG] Nome recebido: {nome}")
    print(f"[DEBUG] Preço máximo recebido: {preco_maximo}")

    caminho = Path(__file__).parent / "products.csv"

    encontrados = []
    categorias = carregar_categorias()
    categoria_id = categorias.get(nome.lower())
    if categoria_id is None:
        for nome_categoria, id_categoria in categorias.items():
            if nome.lower().startswith(nome_categoria[:4]):
                categoria_id = id_categoria
                break
    ultima_consulta["realizada"] = False
    ultima_consulta["resultados"] = []

    with open(caminho, "r", encoding="utf-8-sig") as arquivo:
        produtos = csv.DictReader(arquivo, delimiter=",")

        for produto in produtos:
            if produto["status"].lower() != "active":
                continue
            if nome:
              corresponde_nome = nome.lower() in produto["name"].lower()
              corresponde_categoria = produto["category_id"] == categoria_id

            if not corresponde_nome and not corresponde_categoria:
                continue

            preco = float(produto["price_brl"])

            if preco_maximo is not None and preco > preco_maximo:
                continue

            encontrados.append(produto)

    print("Python consultou o catálogo!")
    
    ultima_consulta["realizada"] = True

    if not encontrados:
        return {"erro": "Nenhum produto encontrado"}

    encontrados.sort(
        key=lambda produto: float(
            produto["price_brl"]
        )
    )
    ultima_consulta["resultados"] = encontrados.copy()
    return {"produtos": encontrados}
if __name__ == "__main__":
    print("Iniciando teste de produtos")

    resultado = consultar_produto(
        nome="violão",
        preco_maximo=500.00
    )

    print(resultado)