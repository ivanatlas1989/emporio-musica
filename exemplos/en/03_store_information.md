# Example 03 — Store Information and Support Channels

## Objective

Demonstrate the agent's ability to retrieve store details from the policy and procedure manual supplied for the challenge.

## Actual Conversation (translated from Portuguese)

**Customer:**  
Address, please.

**Agent:**  
Our address is:

**Rua 14 de Maio, 3200 — Centro**  
Campo Grande, MS, Brazil | Postal code: 79202-333

**Phone / WhatsApp:** (67) 3341-4444

**Opening hours:**

- Monday through Friday: 09:00–18:00
- Saturday: 09:00–13:00
- Sundays and public holidays: closed

We'd be happy to welcome you to try the instruments!

## Visual Evidence

### Address and opening hours

![Store address — original Portuguese conversation](../PRINTS_CHAT/ENDEREÇO_LOJA.png)

### WhatsApp support information

![WhatsApp support](../PRINTS_CHAT/WHATS_APP.png)

## Technical Explanation

Store information is retrieved from the policy and procedures manual.

The `ler_politicas.py` module organizes the PDF into topic-based chunks.

The `consultar_politica()` tool uses embeddings and cosine similarity to identify chunks relevant to the question.

The retrieved passages are supplied to Gemini, which presents the information in natural language.

## Demonstrated Features

- Interpretation of short questions.
- Semantic retrieval of store information.
- Consultation of the PDF manual.
- Natural-language responses.
- Guidance on official support channels.

## Note

The prototype provides the store's contact information but does not send WhatsApp messages or initiate external conversations automatically.
