import streamlit as st
from google import genai

# Page Config
st.set_page_config(
    page_title="AI Companion | Research Study",
    page_icon="💬",
    layout="centered",
)

# Custom Styling for a friendly, calm interface
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Title & Research Notice
st.title("💬 SafeSpace Companion")
st.caption(
    "Part of the research: *Conversational AI Companions: Evaluating Emotional Support Effectiveness for Isolated Cabiao Senior High School Students*"
)

with st.expander("ℹ️ About this Research Session (Read First)"):
    st.write(
        """
        Hello! You are interacting with an experimental AI companion designed to provide a safe, 
        confidential, and supportive space for students feeling isolated or overwhelmed. 
        \n- Your conversation is private and intended to help evaluate emotional support tools.
        \n- Feel free to share what's on your mind—stress, school, or personal feelings.
        """
    )

# Initialize Gemini Client securely via Streamlit Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error(
        "⚠️ GEMINI_API_KEY is missing. Please configure it in your Streamlit Cloud settings."
    )
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
MODEL_ID = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = """
You are a warm, empathetic, and non-judgmental conversational AI companion built specifically to support senior high school students who may be experiencing feelings of isolation, stress, or academic pressure. 
Your goals are to:
1. Practice active listening: Validate their feelings, show genuine care, and ask gentle, open-ended follow-up questions.
2. Provide a safe space to vent without giving overly clinical or robotic advice. Talk like a friendly, supportive peer or mentor.
3. Keep responses concise, warm, and comforting (avoid writing walls of text).
4. If a student mentions severe self-harm, deep crisis, or danger, gently encourage them to reach out to a trusted school counselor, teacher, or parent immediately.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi there! I'm here to chat, listen, or just keep you company. How are you holding up today?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input(
    "Type what's on your mind... (e.g., 'Feeling a bit burnt out today')"
):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    formatted_history = []
    for msg in st.session_state.messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        formatted_history.append({"role": role, "parts": [{"text": msg["content"]}]})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat = client.chats.create(
                    model=MODEL_ID,
                    history=formatted_history,
                    config={"system_instruction": SYSTEM_INSTRUCTION},
                )
                response = chat.send_message(user_prompt)
                bot_reply = response.text

                st.markdown(bot_reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": bot_reply}
                )
            except Exception as e:
                st.error(
                    f"An error occurred while connecting to the AI companion: {e}"
                )
