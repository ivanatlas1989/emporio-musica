# Example 04 — Semantic Interpretation and Return Policy

## Objective

Demonstrate how the agent interprets a customer's change-of-mind return request, retrieves the relevant passages from the policy manual, and provides guidance on the applicable procedure.

## Actual Conversation (translated from Portuguese)

**Customer:**

Regarding my acoustic guitar, which arrived on October 26, 2026: I bought it from you online, but I don't want it anymore. I didn't like it. I want my money back.

**Agent:**

Since your guitar was purchased online and delivered on **October 26, 2026**, today (**November 2, 2026**) you are within the **seven-calendar-day** withdrawal period under the Brazilian Consumer Protection Code.

As a virtual assistant, **I do not have permission to register returns, issue refunds, or schedule pickups directly in the system**.

To proceed with the return and refund, you need to contact the customer support team through the official channels.

The agent also provided contact channels, the return conditions described in the policy, and the need to refer the procedure to the responsible team.

## Visual Evidence

![Semantic interpretation of a return request — original Portuguese conversation](../PRINTS_CHAT/INTERPRETAÇÃO_SEMANTICA_DEVOLUÇÃO.png)

## Processing Evidence

### Backend queries and retrieval of chunks

![Python queries and embeddings](../PRINTS_CHAT/CONSULTAS_PYTHON_BACKEND_EMBEDDINGS_CHUNKS.png)

![Additional processing](../PRINTS_CHAT/CONSULTAS_PYTHON_BACKEND_EMBEDDINGS_CHUNKS_2.png)

## Technical Explanation

The policy and procedure manual was divided into eight topic-based chunks with Python.

Each chunk is converted into a vector representation using `gemini-embedding-001`.

When a policy-related question arrives, the agent invokes `consultar_politica()`.

The tool embeds the question, computes cosine similarity against the chunks, and retrieves the two highest-scoring passages.

Gemini uses the retrieved passages to interpret the request and formulate an answer.

## Intent Interpretation

The customer did not necessarily use the technical terms “right of withdrawal” or “return policy”.

Instead, the customer said:

“I don't want it anymore. I didn't like it. I want my money back.”

The agent semantically associated the request with the return policy for online purchases.

This demonstrates the role of semantic retrieval when customers use informal language.

## Date Handling

The project obtains the current date using Python and the `America/Sao_Paulo` timezone.

For this test:

- Reported delivery date: October 26, 2026.
- Query date: November 2, 2026.
- Elapsed time: 7 calendar days.

The agent's response treated the request as falling within the seven-day withdrawal period, on its final day.

This is a recorded test result, not a substitute for legal or operational verification of the applicable rules.

## Limitations and Operational Safety

The agent does not perform returns, cancellations, or refunds. Instead, it directs customers to the store's official channels.

This restriction is supported by the agent's behavioral instructions and the absence of tools capable of executing those operations.

## Demonstrated Features

- RAG over PDF documents.
- Embedding generation and comparison.
- Semantic similarity retrieval.
- Informal-language interpretation.
- Use of the current date.
- Guidance on deadlines.
- Respect for the prototype's operational boundaries.
