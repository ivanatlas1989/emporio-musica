# Example 02 — Promotions, Inventory, and Conversational Memory

## Objective

Show how the agent interprets questions about promotions, queries structured data, and preserves context across consecutive messages.

## Actual Conversation (translated from Portuguese)

**Customer:**  
I'd like to know whether you have any acoustic guitars on sale...

**Agent:**  
Yes! We currently have two acoustic guitar models on promotion:

1. **Crafter HT-100 Folk Aço Natural**
   - Original price: R$ 2,399.00
   - Promotional price: R$ 1,967.18
   - Discount: 18%

2. **Taylor 110e Dreadnought Natural**
   - Original price: R$ 5,999.00
   - Promotional price: R$ 5,519.08
   - Discount: 8%

**Customer:**  
How many are in stock?

**Agent:**  
We currently have the following quantities in stock for the promotional models:

- Crafter HT-100 Folk Aço Natural: 3 units.
- Taylor 110e Dreadnought Natural: 4 units.

## Visual Evidence

![Promotion query — original Portuguese conversation](../PRINTS_CHAT/CONSULTA_PROMOÇÃO.png)

## Technical Explanation

The agent uses Python lookup functions to access `promotions.csv` and `products.csv`.

Discounts are applied to the products' recorded prices.

In the follow-up question “How many are in stock?”, the customer does not repeat the product names. Gemini uses the conversation history to infer that the question refers to the two guitars previously mentioned.

## Result Validation

| Product | Original price | Discount | Promotional price | Stock |
| --- | ---: | ---: | ---: | ---: |
| Crafter HT-100 | R$ 2,399.00 | 18% | R$ 1,967.18 | 3 |
| Taylor 110e | R$ 5,999.00 | 8% | R$ 5,519.08 | 4 |

The values were checked against the CSV files supplied for the challenge.

## Demonstrated Features

- Active promotion lookup.
- Price and discount retrieval.
- Inventory lookup.
- Conversational memory.
- Context-aware interpretation of follow-up questions.
- Responses grounded in structured data.
