import streamlit as st
import json

st.title("SMP Universes")

# -----------------------------
# LOAD DATABASE
# -----------------------------

with open("database_chatbot.json", "r", encoding="utf-8") as f:
    db = json.load(f)

universes = db.get("universes", [])

# -----------------------------
# DISPLAY UNIVERSES
# -----------------------------

if not universes:
    st.info("No universe data available.")

else:

    for universe in universes:

        st.subheader(universe["name"])
        st.write(universe["description"])

        st.write("Characters:")

        for char in universe["characters"]:

            st.markdown(f"### {char['name']}")

            # TITLE
            title = char.get("title", "")
            if isinstance(title, list):
                st.write("**Title:** " + ", ".join(title))
            elif title:
                st.write(f"**Title:** {title}")

            # DESCRIPTION (only if exists)
            if "description" in char:
                st.write(char["description"])

            # ALLIES
            allies = char.get("allies", [])
            if allies:
                st.write("**Allies:** " + ", ".join(allies))

            # ENEMIES
            enemies = char.get("enemies", [])
            if enemies:
                st.write("**Enemies:** " + ", ".join(enemies))

        st.divider()