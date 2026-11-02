import csv

def consultar_produto(sku):
    with open("produtos.csv", "r", encoding="utf-8-sig") as arquivo:
        produtos = csv.DictReader(arquivo, delimiter=";")

        for produto in produtos:
            if produto["sku"] == sku:
                return produto

    return "Produto não encontrado"


resultado = consultar_produto("999")
print(resultado)