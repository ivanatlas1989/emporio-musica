Empório da Música — Agente de Atendimento com IA Generativa

**Desafio técnico | Processo seletivo Artefact**

1.  Apresentação do projeto

O Empório da Música é uma loja fictícia de instrumentos musicais localizada em Campo Grande/MS. O desafio proposto consiste em desenvolver um protótipo de agente de inteligência artificial capaz de auxiliar a equipe de atendimento, reduzindo a necessidade de intervenção humana em consultas recorrentes.

O agente foi desenvolvido para responder perguntas sobre produtos, preços, disponibilidade, promoções, pedidos e políticas da loja, utilizando os arquivos operacionais e o manual interno fornecidos no desafio.

Meu objetivo foi construir uma solução funcional, com foco na confiabilidade das respostas, na proteção dos dados dos clientes e na simplicidade do fluxo de atendimento.

2.  Tecnologias utilizadas

- **Python:** linguagem principal de desenvolvimento.
- **Google Gemini:** modelo de linguagem responsável pela interpretação das perguntas e geração das respostas.
- **Google GenAI SDK:** integração com os modelos do Google.
- **Google Embedding (`gemini-embedding-001`):** representação vetorial dos trechos do manual.
- **CSV:** fonte de dados estruturados de produtos, clientes, pedidos, itens e promoções.
- **PDF:** fonte documental das políticas e procedimentos da loja.
- **Function Calling:** disponibilização das funções Python ao modelo de linguagem.
- **RAG:** recuperação de informações relevantes do manual por similaridade semântica.
- **Git e GitHub:** versionamento e disponibilização do projeto.

A escolha pelo Gemini considerou a simplicidade da integração via API e a disponibilidade de uma modalidade de uso gratuito sujeita aos limites do provedor.

3. Arquitetura e funcionamento

O projeto foi organizado para separar a interpretação da linguagem natural, a recuperação das informações e a validação dos dados.

O fluxo principal funciona da seguinte maneira:

1. O usuário envia uma pergunta ao agente.
2. O Gemini interpreta a solicitação e identifica a necessidade de consultar alguma fonte.
3. As funções Python responsáveis pelos dados estruturados consultam os arquivos CSV correspondentes.
4. Quando a pergunta envolve políticas e procedimentos, o sistema utiliza busca semântica nos trechos do manual.
5. As informações recuperadas são disponibilizadas ao modelo, que formula uma resposta clara e amigável.
6. Regras adicionais restringem as respostas e determinadas ações, como o acesso a pedidos de terceiros.

Para facilitar a manutenção, organizei as consultas por responsabilidades, utilizando arquivos como `consultar_pedidos.py`, `consultar_produtos.py`, `consultar_promocoes.py`, `consultar_clientes.py` e `ler_politicas.py`.

Essa divisão permite que cada consulta tenha uma responsabilidade específica, evitando concentrar toda a lógica em um único arquivo.

4. Consultas aos dados estruturados

Os arquivos CSV fornecidos são utilizados como fontes de informação operacional.

As consultas foram implementadas com funções Python, utilizando estruturas como `for`, `if` e listas para localizar, selecionar e organizar os registros relevantes.

Por exemplo, quando o usuário pergunta sobre determinado instrumento, o agente pode consultar o catálogo para obter informações reais sobre preço e disponibilidade.

A decisão foi não permitir que o modelo inventasse valores comerciais. As informações devem partir dos dados efetivamente encontrados.

Além do function calling, o projeto utiliza verificações programáticas para realizar consultas obrigatórias ao catálogo em determinadas situações.

5. Interpretação do manual de políticas — RAG

Um dos desafios foi permitir que o agente interpretasse perguntas relacionadas às políticas da loja, mesmo quando o cliente utilizasse palavras diferentes das presentes no manual.

Para isso, implementei um mecanismo de recuperação semântica.

O manual em PDF foi separado em oito trechos (_chunks_), organizados conforme os assuntos abordados, não necessariamente seguindo os limites de cada página.

Em seguida, os trechos foram convertidos em embeddings utilizando o modelo `gemini-embedding-001`, do Google.

Quando o cliente faz uma pergunta sobre políticas, o sistema também gera um embedding da pergunta e calcula a similaridade de cosseno com os vetores dos trechos armazenados.

Os dois trechos com maior similaridade são encaminhados ao agente como contexto para a resposta.

Essa abordagem permite relacionar perguntas como "não gostei do produto e quero devolver" ou "me arrependi da compra" às políticas pertinentes, mesmo sem correspondência literal entre as expressões.

6. Prompt Engineering e limites do agente

Defini instruções para orientar a identidade e o comportamento do atendente virtual.

O agente deve se comunicar em português brasileiro, de maneira cordial, clara e objetiva, mantendo o contexto da Empório da Música.

Também foram estabelecidas restrições:

- Não inventar produtos, preços, estoque ou políticas.
- Não afirmar que realizou operações que não foram executadas.
- Não prometer cancelamentos, reembolsos, devoluções ou agendamentos.
- Consultar as fontes disponíveis antes de responder a perguntas que dependam de dados operacionais.
- Encaminhar ao atendimento humano as solicitações que ultrapassem as capacidades do protótipo.

Essas instruções funcionam como guardrails comportamentais, complementadas por validações no código Python.

7. Segurança dos dados e login simulado

Uma das minhas principais preocupações foi impedir que o agente revelasse informações de pedidos pertencentes a outros clientes.

Como o desafio não exigia um sistema completo de autenticação, optei por simular uma sessão de usuário autenticado.

Exemplo:

```python
cliente_logado = {
    "customer_id": "2",
    "autenticado": True
}
```

A consulta de pedidos utiliza uma função de autorização que verifica se o usuário está autenticado e se o pedido pertence ao mesmo `customer_id`.

Durante os testes, essa abordagem permitiu demonstrar dois comportamentos:

**Consulta autorizada:** o cliente autenticado com ID 2 pode acessar o pedido 8, que pertence a ele.

**Consulta não autorizada:** o mesmo cliente não pode acessar o pedido 2, pertencente ao cliente de ID 7.

A validação é realizada pelo código Python, e não fica exclusivamente a cargo da interpretação do modelo de linguagem.

Trata-se de uma simulação para demonstrar o controle de acesso. Não representa um mecanismo completo de autenticação para produção.

8. Tratamento de datas e prazos

Outro desafio foi interpretar corretamente os prazos estabelecidos nas políticas de atendimento.

Para evitar que o agente utilizasse uma data desatualizada ou presumisse prazos incorretos, foi implementada a obtenção da data atual no fuso horário `America/Sao_Paulo`.

As instruções também orientam o agente a considerar a data de recebimento do produto ao analisar o prazo de arrependimento em compras online, sem presumir informações que não estejam disponíveis.

Quando não existem dados suficientes para uma conclusão, a orientação é solicitar esclarecimentos ou encaminhar o cliente ao atendimento responsável.

9. Memória de conversa

O agente utiliza o recurso de conversação do SDK do Gemini, permitindo manter o histórico do atendimento durante uma sessão.

Isso possibilita interpretar perguntas de continuidade sem exigir que o usuário repita integralmente o contexto anterior.

Também foi implementado um mecanismo simples para manter referências de produtos e preços durante consultas comerciais consecutivas.

A memória utilizada é de sessão, não constituindo armazenamento persistente de históricos entre diferentes execuções.

10. Processo de desenvolvimento e uso de IA

Fui responsável pela concepção da solução, definição da arquitetura, organização dos módulos, planejamento das consultas, desenho do fluxo de atendimento e estabelecimento das regras de comportamento e autorização.

Participei das decisões sobre tratamento de dados, recuperação semântica, memória de conversa, uso de ferramentas e validação das respostas.

Para a implementação e depuração do código Python, utilizei inteligência artificial como ferramenta de assistência, especialmente na escrita de funções, identificação de erros e refinamento das implementações.

O processo foi conduzido de maneira interativa, com decisões sobre o comportamento esperado, execução de testes e ajustes conforme os resultados observados.

O projeto começou a ser desenvolvido localmente e foi posteriormente integrado ao GitHub. Por esse motivo, o histórico de commits não representa integralmente todas as etapas iniciais de desenvolvimento.

11. Limitações do protótipo

O projeto foi construído para demonstrar a solução no contexto do desafio técnico, não para representar um sistema completo de atendimento em produção.

Entre suas limitações estão:

- Autenticação simulada, sem um provedor real de identidade.
- Informações operacionais obtidas de arquivos CSV fornecidos para o desafio.
- Ausência de integração com sistemas reais de pedidos, pagamentos e logística.
- Impossibilidade de executar alterações operacionais, como reembolsar ou cancelar pedidos.
- Dependência da API do Gemini para interpretação e geração de respostas.
- Necessidade de testes adicionais de segurança, robustez e qualidade antes de qualquer utilização em produção.

12. Considerações finais

Minha principal preocupação durante o desenvolvimento foi construir um agente que não apenas conversasse com o cliente, mas que consultasse as informações necessárias para fornecer respostas fundamentadas.

A solução combina recuperação estruturada de dados, busca semântica, instruções comportamentais e validações programáticas, procurando equilibrar flexibilidade de linguagem com controle sobre as informações fornecidas.

O projeto também foi uma oportunidade de aplicar conceitos de IA generativa a um cenário de negócio, enfrentando questões práticas de arquitetura, confiabilidade, privacidade e experiência do usuário.

O resultado é um protótipo funcional que demonstra uma abordagem para automatizar atendimentos recorrentes, preservando limites claros para consultas sensíveis e operações que exigem intervenção humana.
Como complemento à entrega do desafio técnico, disponibilizei uma versão online do agente de atendimento do Empório da Música, permitindo que a equipe avaliadora interaja diretamente com a solução e teste suas funcionalidades.

Durante os testes, a modalidade gratuita da API do Google Gemini apresentou instabilidades frequentes, principalmente erros http503. Para resolver, optei por utilizar o modelo Gemini 3.6 Flash, com créditos habilitados na API.

Após essa alteração, o agente funcionou perfeitamente nos testes realizados, incluindo consultas ao catálogo, promoções, políticas da loja e pedidos, com validação de autorização de acesso.

Link para acessar o agente:
https://emporio-musica-6bpwrdwas5yn93husv5mar.streamlit.app/
