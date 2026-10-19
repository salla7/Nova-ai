
import streamlit as st

st.set_page_config(
    page_title="Independent AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Independent AI Chatbot")
st.caption("An independent AI assistant powered by artificial intelligence.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I'm your AI chatbot. "
                "Ask me a question to get started."
            ),
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    answer = (
        "Thanks for your question! This chatbot interface is ready. "
        "The AI engine will be connected in the next step."
    )

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
