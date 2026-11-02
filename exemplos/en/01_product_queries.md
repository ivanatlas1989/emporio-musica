# Example 01 — Product Queries

## Objective

Demonstrate the agent's ability to query the product catalog supplied as CSV data and answer questions about musical instruments, pricing, and availability.

## Scenario

A customer wants information about instruments available at the store.

The agent uses Python functions to query structured catalog data instead of relying solely on the language model's prior knowledge.

## Execution Evidence

### Catalog lookup

![Product query](../PRINTS_CHAT/CONSULTA_PRODUTOS.png)

### Price lookup — Takamine GD20

![Takamine GD20 lookup](../PRINTS_CHAT/CONSULTA_TAKAMINE_GD20.png)

### Lowest-priced ukulele query

![Ukulele query](../PRINTS_CHAT/UKELELE_MAIS_BARATO.png)

## Technical Implementation

The lookup is performed by `consultar_produtos.py`, using data from `products.csv`.

Gemini interprets the user's request and can invoke the lookup function to retrieve catalog information. The response is built using the records found.

## Demonstrated Features

- Product search by name or model.
- Retrieval of recorded prices.
- Availability checks.
- Natural-language question interpretation.
- Integration between Gemini and Python functions.
