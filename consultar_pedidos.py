import csv
from pathlib import Path

def consultar_itens_pedido(numero_pedido: str) -> list:
    caminho = Path(__file__).parent / "order_items.csv"
    itens_encontrados = []

    with open(caminho, "r", encoding="utf-8-sig") as arquivo:
        itens = csv.DictReader(arquivo, delimiter=",")

        for item in itens:
            if item["order_id"] == str(numero_pedido):
                itens_encontrados.append(item)

    return itens_encontrados

def consultar_pedido(numero_pedido: str) -> dict:
    caminho = Path(__file__).parent / "orders.csv"

    with open(caminho, "r", encoding="utf-8-sig") as arquivo:
        pedidos = csv.DictReader(arquivo, delimiter=",")

        for pedido in pedidos:
            if pedido["order_id"] == str(numero_pedido):
                print("[PEDIDOS] Pedido encontrado!")
                return pedido

    return {"erro": "Pedido não encontrado"}

def consultar_pedido_autorizado(numero_pedido: str, cliente_logado: dict) -> dict:
    if not cliente_logado.get("autenticado"):
        return {"erro": "Cliente não autenticado"}

    pedido = consultar_pedido(numero_pedido)

    if "erro" in pedido:
        return pedido

    if pedido["customer_id"] != cliente_logado["customer_id"]:
        return {"erro": "Acesso não autorizado a este pedido"}

    pedido["itens"] = consultar_itens_pedido(numero_pedido)

    return pedido

if __name__ == "__main__":
    cliente_logado = {
        "customer_id": "2",
        "autenticado": True
    }

    print("Teste 1:", consultar_pedido_autorizado("8", cliente_logado))

    cliente_logado["customer_id"] = "3"

    print("Teste 2:", consultar_pedido_autorizado("8", cliente_logado))