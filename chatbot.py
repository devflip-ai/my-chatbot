import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Page config
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS to make it look like ChatGPT
st.markdown("""
    <style>
        .stChatMessage { padding: 10px; border-radius: 10px; margin: 5px 0; }
        .stChatInputContainer { position: fixed; bottom: 0; }
        #MainMenu, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 My AI Chatbot")
st.caption("Powered by Groq + Llama 3")

# Initialize Groq client
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

SYSTEM_PROMPT = """You are a helpful, friendly AI assistant.
You remember everything the user tells you during this conversation.
Always refer back to earlier context when relevant."""

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Message the chatbot..."):

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call Groq API with full history
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages
                ]
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})