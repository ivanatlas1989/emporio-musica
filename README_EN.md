# Empório da Música — Generative AI Customer Support Agent

**Technical challenge | Artefact recruitment process**

## 1. Project Overview

Empório da Música is a fictional musical instrument store located in Campo Grande, Mato Grosso do Sul, Brazil. The challenge was to prototype an AI agent that helps the customer support team handle recurring questions and reduces the need for manual intervention.

The agent answers questions about products, prices, availability, promotions, orders, and store policies using the operational datasets and internal policy manual supplied for the challenge.

My goal was to build a functional solution focused on reliable answers, customer data protection, and a straightforward support workflow.

## 2. Technologies Used

- **Python:** primary implementation language.
- **Google Gemini:** language model for interpreting questions and generating answers.
- **Google GenAI SDK:** integration with Google's models.
- **Google Embeddings (`gemini-embedding-001`):** vector representations of policy manual excerpts.
- **CSV files:** structured data for products, customers, orders, order items, and promotions.
- **PDF:** source document for store policies and procedures.
- **Function calling:** exposes Python functions to the model.
- **Retrieval-Augmented Generation (RAG):** retrieves relevant policy excerpts via semantic similarity.
- **Streamlit:** web-based chat interface.
- **Git and GitHub:** source control and project delivery.

Gemini was selected for the simplicity of its API integration and the availability of an initial free usage tier, subject to provider limits.

## 3. Architecture and Workflow

The project separates natural language interpretation, information retrieval, and data validation.

The main workflow is:

1. A user submits a question to the agent.
2. Gemini interprets the request and determines which information sources are needed.
3. Python functions query the relevant CSV files for structured data.
4. Questions about store procedures and policies trigger semantic retrieval from the policy manual.
5. Retrieved information is supplied to the model to produce a clear, helpful response.
6. Additional safeguards constrain responses and sensitive operations, including access to orders belonging to other customers.

The source code is divided by responsibility across modules such as `consultar_pedidos.py`, `consultar_produtos.py`, `consultar_promocoes.py`, `consultar_clientes.py`, and `ler_politicas.py`. This structure keeps each query focused and avoids concentrating the entire implementation in one file.

## 4. Structured Data Queries

The supplied CSV files are the operational information sources.

Python functions use basic structures such as `for` loops, `if` statements, and lists to find and organize relevant records. For example, when asked about a particular instrument, the agent can retrieve its recorded price and availability from the catalog.

The model is instructed not to fabricate commercial values; such facts must come from available data. In addition to function calling, programmatic checks trigger mandatory catalog lookups in certain situations.

## 5. Policy Manual Retrieval — RAG

A central challenge was answering policy-related questions even when customers used wording different from the original manual.

I implemented semantic retrieval to address this. The PDF manual is divided into eight topic-based text chunks, which do not necessarily align with page boundaries.

Each chunk is converted into an embedding using Google's `gemini-embedding-001` model. When a user asks a policy question, the system embeds the query, computes cosine similarity against the stored chunk vectors, and selects the two most similar chunks as context for the language model.

This approach helps connect phrases such as “I don't like the product and want to return it” or “I changed my mind about the purchase” to the applicable policies without requiring exact keyword matches.

## 6. Prompt Engineering and Agent Boundaries

I defined instructions for the virtual assistant's identity and behavior. The agent should communicate clearly, politely, and concisely in Brazilian Portuguese, reflecting the store's customer support context.

The instructions also specify that the agent must:

- Not invent products, prices, stock levels, or policies.
- Not claim to have performed actions that were not executed.
- Not promise cancellations, refunds, returns, or appointments.
- Consult the available sources before answering questions that depend on operational information.
- Refer requests beyond the prototype's capabilities to human support.

These behavioral guardrails are complemented by programmatic validations in Python.

## 7. Customer Data Protection and Simulated Login

A key concern was preventing disclosure of order details belonging to another customer.

Because a complete authentication system was outside the challenge's scope, I used a simulated authenticated session:

```python
cliente_logado = {
    "customer_id": "2",
    "autenticado": True
}
```

The order lookup calls an authorization function that checks authentication and compares the order's `customer_id` with the signed-in customer's ID.

For example, simulated customer 2 is authorized to view order 8, which belongs to that customer, but is denied access to order 2, which belongs to customer 7. The same ownership check applies to all orders, not just these examples.

This validation takes place in Python rather than relying solely on the language model's interpretation. The login is a demonstration mechanism, not production-grade authentication.

## 8. Dates and Deadlines

The prototype obtains the current date in the `America/Sao_Paulo` timezone to avoid relying on a stale or assumed date.

The instructions also guide the model to consider the product receipt date when discussing withdrawal periods for online purchases and to avoid inventing missing facts.

If the information is insufficient to draw a conclusion, the agent should ask for clarification or refer the customer to the appropriate support team.

## 9. Conversation Memory

The agent uses the Gemini SDK's chat functionality to maintain conversational history within a session. This makes it possible to interpret follow-up questions without requiring the customer to repeat all prior context.

A simple mechanism also tracks product and price references across consecutive commercial questions.

Conversation history is session-scoped and is not persisted across independent runs.

## 10. Development Process and AI-Assisted Coding

I was responsible for designing the solution, defining the architecture, organizing modules, planning the data queries, designing the support workflow, and setting behavior and authorization rules.

I participated in decisions concerning data handling, semantic retrieval (RAG), conversation memory, tool usage, and response validation.

I used **ChatGPT (OpenAI)** as a development assistant, particularly for drafting and reviewing Python functions, troubleshooting errors, integrating with the Gemini API, and building the Streamlit interface.

My workflow was iterative: I defined requirements and expected behavior, discussed implementation alternatives with the assistant, ran the code, analyzed outcomes, and requested adjustments when necessary.

Architecture, business rules, order-access validation, and agent behavior were guided by the challenge objectives. AI assistance supported implementation, debugging, and learning throughout development.

Development started locally and was later integrated with GitHub. Accordingly, the commit history does not capture every initial development step.

## 11. Known Limitations

This is a technical-challenge prototype, not a production-ready customer support system.

Known limitations include:

- Simulated authentication rather than a real identity provider.
- Operational information stored in the supplied CSV files.
- No integration with live ordering, payment, or shipping systems.
- No capability to execute operational changes such as refunds or order cancellations.
- Dependence on the Gemini API for understanding questions and generating responses.
- Additional security, resilience, and answer-quality testing would be necessary before production deployment.

## 12. Final Considerations and Online Demo

My main objective was to build an agent that does more than converse: it consults relevant information to provide grounded answers.

The implementation combines structured data retrieval, semantic search, behavioral instructions, and programmatic checks to balance natural-language flexibility with control over the facts presented.

The challenge also provided an opportunity to apply generative AI concepts to a realistic business scenario and explore architecture, reliability, privacy, and user-experience tradeoffs.

An online version of the agent is available so reviewers can interact directly with the prototype:

**Live demo:** https://emporio-musica-6bpwrdwas5yn93husv5mar.streamlit.app/

During development, the initial free-tier Gemini API usage frequently returned HTTP 503 errors. I enabled paid API credits and selected the **Gemini 3.6 Flash** model. Subsequent tests successfully covered catalog queries, promotions, store policies, and authorization-controlled order lookups. The service remains subject to the provider's availability.

## 13. Running the Project Locally

### Prerequisites

- Python 3.11 or later.
- A Google Gemini API key.
- Internet access.

### Installation

Clone the repository:

```bash
git clone https://github.com/ivanatlas1989/emporio-musica.git
cd emporio-musica
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### API Configuration

Create a `.env` file in the project root with:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

The API key can be obtained through Google AI Studio. **Never commit the actual `.env` file or API key to GitHub.**

### Run the Web Interface

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL, typically `http://localhost:8501`.

### Run in the Terminal

```bash
python gemini.py
```

### Online Demo

The hosted prototype can also be tested in a browser:

https://emporio-musica-6bpwrdwas5yn93husv5mar.streamlit.app/

### Simulated Authentication

The demonstration uses a simulated authenticated session for customer ID 2.

- **Order owned by customer 2:** access is allowed.
- **Order owned by another customer:** access is denied, regardless of order number.
- **Nonexistent order:** the system reports that it cannot find the order.

For example, order 8 is accessible and order 2 is blocked. Authorization is checked in the Python backend rather than left solely to the language model. This is not a substitute for real user authentication.

## 14. Future Improvements

With more development time, I would prioritize:

1. **Real authentication:** replace the simulated session with an actual login system and per-user access controls.
2. **Live system integrations:** replace CSV-based sources with database or API queries for products, inventory, orders, and customers.
3. **Automated testing:** test queries, calculations, policy application, and unauthorized access attempts.
4. **RAG optimization:** cache the manual's embeddings rather than recomputing them on startup.
5. **API resilience:** add controlled retries, temporary error handling, and fallback behavior for HTTP 503 responses.
6. **Monitoring:** track response latency, token consumption, API costs, and answer quality.
7. **Systematic evaluation:** develop a benchmark of expected questions and answers to assess query accuracy, policy retrieval, and safety.

These improvements would help evolve the prototype into a more robust, scalable solution suitable for a production environment.

---

**Conversation examples:** see the five documented scenarios in the [`exemplos/` directory](exemplos/), including catalog queries, promotions, store information, returns, and order authorization.
