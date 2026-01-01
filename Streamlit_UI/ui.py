import os
import sys
import json
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from Core.agent import router  # router-based backend

HISTORY_FILE = os.path.join(BASE_DIR, "chat_history.json")

st.set_page_config(
    page_title="Sunbeam Chatbot",
    page_icon="🤖",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "theme" not in st.session_state:
    st.session_state.theme = "light"

def apply_theme(theme: str):
    if theme == "dark":
        st.markdown(
            """
            <style>
            body, .stApp {
                background-color: #0e1117;
                color: #ffffff;
            }

            div[data-testid="stChatMessageContent"] {
                background-color: #1e1e1e;
                color: #ffffff;
                border-radius: 10px;
                padding: 10px;
            }

            textarea, input {
                background-color: #1e1e1e !important;
                color: #ffffff !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            body, .stApp {
                background-color: #ffffff;
                color: #000000;
            }

            div[data-testid="stChatMessageContent"] {
                background-color: #f1f3f6;
                color: #000000;
                border-radius: 10px;
                padding: 10px;
            }

            textarea, input {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

apply_theme(st.session_state.theme)

with st.sidebar:
    st.title("⚙️ Settings")

    theme_choice = st.radio(
        "Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == "light" else 1
    )

    if theme_choice.lower() != st.session_state.theme:
        st.session_state.theme = theme_choice.lower()
        st.rerun()

    st.divider()

    if st.button("💾 Save Chat"):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, indent=2)
        st.success("Chat saved successfully")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Sunbeam Chatbot")

# chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask your question...")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    response = router(user_input)

    # Add bot message
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.markdown(response)
