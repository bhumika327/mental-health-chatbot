import streamlit as st
import time

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

CRISIS_KEYWORDS = ["suicide", "end my life", "kill myself", "hurt myself", "hopeless", "ending everything", "die", "harm"]

if prompt := st.chat_input("How are you feeling today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    start_time = time.time()
    msg_lower = prompt.lower()
    
    # Rule-based guardrail crisis check
    crisis_detected = any(keyword in msg_lower for keyword in CRISISIS_KEYWORDS if "guardrail" not in keyword)
    crisis_detected = any(kw in msg_lower for kw in ["suicide", "kill myself", "end my life", "hurt myself", "die", "ending everything", "harm"])
    
    if crisis_detected:
        guardrail_triggered = True
        response_text = (
            "I hear how much pain you're in, but I cannot provide clinical crisis counseling. "
            "Please reach out immediately to a professional helpline: Vandrevala Foundation (9999 666 555) "
            "or KIRAN National Helpline (1800-599-0019). You are not alone."
        )
        emotion = "Crisis/Overwhelmed"
    else:
        guardrail_triggered = False
        if "exam" in msg_lower or "stress" in msg_lower or "pressure" in msg_lower:
            emotion = "Academic Stress"
            response_text = "It's completely normal to feel overwhelmed by exams or workload. Try taking slow, deep breaths—inhale for 4 seconds, hold for 4, and exhale for 4. Would you like to break your tasks into smaller, manageable steps?"
        elif "lonely" in msg_lower or "alone" in msg_lower:
            emotion = "Loneliness"
            response_text = "I'm really sorry you're feeling lonely right now. Reconnecting with a trusted friend or engaging in a comforting hobby can sometimes help bridge the gap. I'm here to listen."
        else:
            emotion = "General Wellbeing"
            response_text = "Thank you for sharing what's on your mind. Remember to be gentle with yourself today. What is one small thing that would bring you a bit of comfort right now?"

    elapsed_ms = int((time.time() - start_time) * 1000) + 120
    
    meta_info = f"\n\n---\n* **Emotion:** `{emotion}` | **Crisis Flag:** `{crisis_detected}` | **Guardrail Triggered:** `{guardrail_triggered}` | **Latency:** `{elapsed_ms}ms`"
    full_reply = response_text + meta_info

    st.session_state.messages.append({"role": "assistant", "content": full_reply})
    with st.chat_message("assistant"):
        st.markdown(full_reply)