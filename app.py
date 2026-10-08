"""Streamlit web interface. Run with: streamlit run app.py"""
import uuid

import streamlit as st

from assistant import ask, build_agent

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 AI Assistant with LangChain")

if "agent" not in st.session_state:
    st.session_state.agent = build_agent()
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []

with st.sidebar:
    st.header("About")
    st.write("Built with LangChain + Gemini. It remembers your conversation and can use tools.")
    st.caption("Tools: calculator, Wikipedia search, current time")
    if st.button("🗑️ New chat"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = ask(st.session_state.agent, prompt, st.session_state.thread_id)
            except Exception as e:
                reply = f"Something went wrong: {e}"
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
