import os
import requests
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="PsychPal", page_icon="💬", layout="centered")
st.title("Talk to PsychPal!")

# ---------- Backend URL ----------
BACKEND_URL = os.getenv("CS3249_BACKEND_URL", "http://localhost:8000")

# ---------- Clear button ----------
if st.button("Clear Conversation"):
    st.session_state.history = []
    try:
        requests.post(f"{BACKEND_URL}/reset", timeout=5)
    except Exception as e:
        st.error(f"Failed to reset backend: {e}")

# ---------- Initialize history ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Render history ----------
for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.write(turn["content"])


# ---------- Message sender ----------
def send_to_backend(user_text: str) -> dict:
    """POST to backend and return assistant text (or error)."""
    payload = {
        "message": user_text,
    }
    try:
        resp = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"response": f"[Frontend error: {e}]", "safety_action": "allow"}


# ---------- Chat input ----------
if "blocked" not in st.session_state:
    st.session_state.blocked = False

if st.session_state.blocked:
    st.error("This conversation has been blocked due to safety concerns.")
    st.link_button("Get Help", "https://www.sos.org.sg/our-services/#tab-one")
    st.stop()

user_input = st.chat_input("Type your message and press Enter")
if user_input:
    # show user message
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # get assistant reply
    reply_data = send_to_backend(user_input)
    reply = reply_data.get("response") or ""
    st.session_state.history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)

    if reply_data.get("safety_action") == "block":
        st.session_state.blocked = True
        st.rerun()

