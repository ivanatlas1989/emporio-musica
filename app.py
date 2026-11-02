import streamlit as st
from gemini import cliente, configuracao

# Configuração da página
st.set_page_config(
    page_title="Empório da Música",
    page_icon="🎸",
    layout="centered"
)

# Conversa independente por sessão
if "chat" not in st.session_state:
    st.session_state.chat = cliente.chats.create(
       model="gemini-3.6-flash",
        config=configuracao
    )

# Histórico visual das mensagens
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Interface
st.title("🎸 Empório da Música")
st.caption("Atendimento virtual com Inteligência Artificial")

st.chat_message("assistant").write(
    "Olá! Bem-vindo ao Empório da Música! "
    "Como posso ajudar você hoje?"
)

# Mostrar mensagens anteriores
for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["papel"]):
        st.write(mensagem["conteudo"])

# Campo de mensagem
pergunta = st.chat_input("Digite sua mensagem...")

if pergunta:
    st.session_state.mensagens.append({
        "papel": "user",
        "conteudo": pergunta
    })

    with st.chat_message("user"):
        st.write(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando o atendente..."):
            try:
                resposta = st.session_state.chat.send_message(
                    pergunta
                )

                texto = resposta.text or (
                    "Não consegui gerar uma resposta."
                )

            except Exception as erro:
                print("[ERRO GEMINI]:", erro)
                texto = (
                    "Não consegui concluir sua consulta agora. "
                    "Por favor, tente novamente."
                )

            st.write(texto)

    st.session_state.mensagens.append({
        "papel": "assistant",
        "conteudo": texto
    })