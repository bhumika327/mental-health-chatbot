import streamlit as st
import requests

st.set_page_config(page_title="Mental Health Support Chatbot", page_icon="🌿", layout="centered")

st.title("🌿 Chatbot for Mental Health Awareness (Non-Clinical)")
st.markdown("A safe, empathetic companion offering supportive guidance with rule-based safety guardrails and crisis escalation.")

# Disclaimer box
st.warning("⚠️ **Disclaimer:** This chatbot provides non-clinical emotional support and psychoeducational guidance only. It is not a substitute for professional psychiatric care or medical therapy.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "sess_mh_001"

st.sidebar.header("Session Settings")
session_id_input = st.sidebar.text_input("Session ID", value=st.session_state.session_id)
if session_id_input != st.session_state.session_id:
    st.session_state.session_id = session_id_input
    st.session_state.messages = []

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How are you feeling today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"session_id": st.session_state.session_id, "message": prompt}
        )
        if response.status_code == 200:
            data = response.json()
            bot_reply = data["response"]
            
            meta_info = f"\n\n---\n* **Emotion:** `{data['detected_emotion']}` | **Crisis Flag:** `{data['crisis_detected']}` | **Guardrail Triggered:** `{data['guardrail_triggered']}` | **Latency:** `{data['response_time_ms']}ms`"
            full_reply = bot_reply + meta_info
        else:
            full_reply = "Error connecting to backend service."
    except Exception as e:
        full_reply = f"Could not connect to FastAPI server at `http://127.0.0.1:8000`. Make sure it is running! Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": full_reply})
    with st.chat_message("assistant"):
        st.markdown(full_reply)
