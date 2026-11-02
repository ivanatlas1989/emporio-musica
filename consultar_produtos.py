import csv
from pathlib import Path
ultima_consulta = {
    "realizada": False,
    "resultados": []
}


def consultar_produto(
    nome: str = "",
    preco_maximo: float | None = None
) -> dict:
    """Consulta instrumentos por nome e preço máximo."""

    print(f"[DEBUG] Nome recebido: {nome}")
    print(f"[DEBUG] Preço máximo recebido: {preco_maximo}")

    caminho = Path(__file__).parent / "produtos.csv"

    encontrados = []
    ultima_consulta["realizada"] = True

    with open(caminho, "r", encoding="utf-8-sig") as arquivo:
        produtos = csv.DictReader(arquivo, delimiter=";")

        for produto in produtos:
            if nome and nome.lower() not in produto["nome"].lower():
                continue

            preco = float(produto["preco"].replace(",", "."))

            if preco_maximo is not None and preco > preco_maximo:
                continue

            encontrados.append(produto)

    print("Python consultou o catálogo!")

    if not encontrados:
        return {"erro": "Nenhum produto encontrado"}

    encontrados.sort(
        key=lambda produto: float(
            produto["preco"].replace(",", ".")
        )
    )
    ultima_consulta["resultados"] = encontrados.copy()
    return {"produtos": encontrados}
if __name__ == "__main__":
    print("Iniciando teste de produtos")

    resultado = consultar_produto(
        nome="Violão",
        preco_maximo=500
    )

    print(resultado)