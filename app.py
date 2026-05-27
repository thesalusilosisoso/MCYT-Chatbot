import streamlit as st
import json
import os

FILE_DB = "database_chatbot.json"

with open(FILE_DB,"r") as f:
    json.load(f)

st.set_page_config(page_title="MCYT Lore")

# -----------------------------
# HOME PAGE
# -----------------------------

def home():

    st.title("MCYT Lore")

    st.write("""
    Welcome to the MCYT Lore Chatbot!

    This application allows users to:
    - Explore SMP universes
    - View character information
    - Ask lore questions
    - Learn about events and stories

    Use the sidebar to navigate through the app.
    """)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("Navigation")

pages = [
    st.Page(home, title="Home", default=True),
    st.Page("pages/universes.py", title="Universes"),
    st.Page("pages/chatbot.py", title="Chatbot"),
    st.Page("pages/about.py", title="About")
]

pg = st.navigation(pages)
pg.run()
