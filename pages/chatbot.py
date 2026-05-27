import streamlit as st
import os
from pathlib import Path
from google import genai
import json

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="MCYT Lore Chatbot")
st.title("MCYT Lore Chatbot")

# -----------------------------
# API KEY
# -----------------------------
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# -----------------------------
# LOAD JSON DATABASE
# -----------------------------
try:
    with open("database_chatbot.json", "r", encoding="utf-8") as f:
        db = json.load(f)
except FileNotFoundError:
    db = {"universes": []}

# -----------------------------
# BUILD STRUCTURED LORE CONTEXT
# -----------------------------
lore_context = ""

for universe in db.get("universes", []):

    lore_context += f"""
========================
UNIVERSE: {universe['name']}
DESCRIPTION: {universe['description']}
========================

CHARACTERS:
"""

    for char in universe.get("characters", []):
        lore_context += f"""
- Name: {char.get('name')}
- Title: {char.get('title')}
- Allies: {char.get('allies')}
- Enemies: {char.get('enemies')}
- Source: Official wiki reference
"""

    lore_context += "\n\n"

# -----------------------------
# SYSTEM INSTRUCTION (IMPORTANT)
# -----------------------------
system_instruction = f"""
ou are a Minecraft lore assistant.

You answer ONLY using the provided database and wiki reference content.

IMPORTANT RULES:
- DO NOT show URLs or wiki links in your answer.
- DO NOT say "you can visit" or reference links.
- Instead, summarize the information naturally.
- Use wiki sources ONLY as background knowledge.
- If you are unsure, say: "I don't have enough information in the lore database."

STYLE:
- Explain characters like a lore encyclopedia
- Keep responses clear and immersive

LORE DATABASE:
{lore_context}
"""

# -----------------------------
# CHAT MEMORY
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "text": "Hello! Ask me anything about MCYT SMP lore."
        }
    ]

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# -----------------------------
# USER INPUT
# -----------------------------
question = st.chat_input("Ask about SMP lore...")

if question:

    # Show user message
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.chat_history.append(
        {"role": "user", "text": question}
    )

    # Build conversation context
    conversation = ""

    for msg in st.session_state.chat_history:
        conversation += f"{msg['role']}: {msg['text']}\n"

    final_prompt = system_instruction + "\n\nCHAT HISTORY:\n" + conversation

    # AI RESPONSE
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=final_prompt
                )
                answer = response.text

            except Exception as e:
                answer = f"System error: {e}"

            st.markdown(answer)

    # Save response
    st.session_state.chat_history.append(
        {"role": "assistant", "text": answer}
    )