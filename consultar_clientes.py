import csv
from pathlib import Path


def consultar_cliente(customer_id: str) -> dict:
    caminho = Path(__file__).parent / "customers.csv"

    with open(caminho, "r", encoding="utf-8-sig") as arquivo:
        clientes = csv.DictReader(arquivo, delimiter=",")

        for cliente in clientes:
            if cliente["customer_id"] == str(customer_id):
                return cliente

    return {"erro": "Cliente não encontrado"}


if __name__ == "__main__":
    resultado = consultar_cliente("2")
    print(resultado)