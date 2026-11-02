import csv
from pathlib import Path

def consultar_promocoes() -> dict:
    caminho = Path(__file__).parent / "promotions.csv"
    encontradas = []
    caminho_produtos = Path(__file__).parent / "products.csv"

    with open(caminho_produtos, "r", encoding="utf-8-sig") as arquivo:
      produtos = {
        produto["product_id"]: produto
        for produto in csv.DictReader(arquivo)
      }

      with open(caminho, "r", encoding="utf-8-sig") as arquivo:
        promocoes = csv.DictReader(arquivo)

        for promocao in promocoes:
            if promocao["is_active"] == "1":
                produto = produtos.get(promocao["product_id"])

                if produto and produto["status"].lower() == "active":
                    preco = float(produto["price_brl"])
                    desconto = float(promocao["discount_percent"])

                    promocao["nome_produto"] = produto["name"]
                    promocao["preco_original"] = round(preco, 2)
                    promocao["preco_promocional"] = round(
                        preco * (1 - desconto / 100), 2
                    )

                    encontradas.append(promocao)

    return {"promocoes": encontradas}


if __name__ == "__main__":
    print(consultar_promocoes())