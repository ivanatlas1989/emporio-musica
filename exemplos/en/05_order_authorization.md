# Example 05 — Order Security and Authorization

## Objective

Demonstrate how the agent protects order information by allowing access only when an order belongs to the authenticated customer.

## Scenario

The challenge prototype implements simulated authentication. Customer ID 2 is treated as authenticated:

```python
cliente_logado = {
    "customer_id": "2",
    "autenticado": True
}
```

The authenticated customer identity is predetermined in the Python backend, not selected by the language model.

## Test 1 — Authorized Order

**Customer (translated from Portuguese):**

I'd like to check the status of my order number 8.

**Result:**

The system locates order 8, verifies that it belongs to customer ID 2, and allows access.

**Order details:**

- Order number: 8
- Owning customer ID: 2
- Recorded status: `shipped`
- Amount: R$ 349.90
- Tracking number: BRJL5544332BR

### Visual Evidence

![Authorized order query — original Portuguese conversation](../PRINTS_CHAT/BUSCA_PEDIDO.png)

## Test 2 — Unauthorized Order

**Customer (translated from Portuguese):**

I'd like to check order number 2.

**Agent response (translated):**

“I'm sorry, but I couldn't access the details of order number 2. The system indicates that I'm not authorized to view this particular order.”

Order 2 exists but belongs to customer ID 7. Because the simulated authenticated customer has ID 2, the lookup is blocked.

### Visual Evidence

![Unauthorized order query — original Portuguese conversation](../PRINTS_CHAT/BLOQUEIO_PEDIDO_NÃO_ESTÁ_LOGADO_NA_CONTA_CORRETA.png)

## Technical Implementation

Authorization is implemented in `consultar_pedidos.py`.

The `consultar_pedido_autorizado()` function performs these steps:

1. Confirms that the customer is authenticated.
2. Looks up the requested order in `orders.csv`.
3. Checks whether the order was found.
4. Compares the order's `customer_id` with the authenticated customer's ID.
5. Grants access only when the identifiers match.

Implementation excerpt (original Portuguese error strings retained):

```python
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
```

## Architectural Decision

Authorization does not depend exclusively on the prompt or Gemini's interpretation.

The model can request a lookup, but the Python function decides whether the requested data may be disclosed.

This separation reduces the risk of exposing other customers' data due to inappropriate model responses.

## Limitations

The prototype uses a predetermined simulated identity.

There is no actual login, authenticated-session management, or integration with an identity provider.

Production deployment would require real authentication, secure session handling, and further authorization tests.

## Demonstrated Features

- CSV-based order queries.
- Simulated authenticated customer.
- Order ownership validation.
- Blocking access to other customers' data.
- Separation of authorization decisions from language generation.
- Handling unauthorized requests.
