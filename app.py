import streamlit as st
import json
import os

st.title("📝 Meine To-do-Liste")

if "name" not in st.session_state:
    st.session_state.name = ""

if st.session_state.name == "":
    st.write("Wie heißt du?")
    eingegebener_name = st.text_input("Dein Name:")
    if st.button("Los geht's"):
        if eingegebener_name.strip():
            st.session_state.name = eingegebener_name.strip()
            st.rerun()
    st.stop()

st.write(f"Hallo, {st.session_state.name}! 👋")

DATEI = f"aufgaben_{st.session_state.name}.json"

if "aufgaben" not in st.session_state:
    if os.path.exists(DATEI):
        with open(DATEI, "r", encoding="utf-8") as f:
            st.session_state.aufgaben = json.load(f)
    else:
        st.session_state.aufgaben = []

def speichern():
    with open(DATEI, "w", encoding="utf-8") as f:
        json.dump(st.session_state.aufgaben, f, ensure_ascii=False, indent=2)

with st.form("neue_aufgabe_form", clear_on_submit=True):
    neue_aufgabe = st.text_area("Neue Aufgabe eingeben:", height=80)
    abgeschickt = st.form_submit_button("Hinzufügen")

if abgeschickt and neue_aufgabe:
    st.session_state.aufgaben.append({"text": neue_aufgabe, "erledigt": None})
    speichern()

st.subheader("Deine Aufgaben:")

def textbox(text):
    return f"""
    <div style="
        border: 2px solid #cccccc;
        border-radius: 6px;
        padding: 10px;
        min-height: 20px;
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-wrap: break-word;
    ">{text}</div>
    """

css_regeln = ""
zu_loeschen = None

for i, aufgabe in enumerate(st.session_state.aufgaben):
    st.markdown(textbox(aufgabe["text"]), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    haken_farbe = "limegreen" if aufgabe["erledigt"] is True else "var(--secondary-background-color)"
    kreuz_farbe = "red" if aufgabe["erledigt"] is False else "var(--secondary-background-color)"
    haken_icon_farbe = "white" if aufgabe["erledigt"] is True else "var(--text-color)"
    kreuz_icon_farbe = "white" if aufgabe["erledigt"] is False else "var(--text-color)"

    css_regeln += f"""
    .st-key-haken_{i} button {{
        background-color: {haken_farbe} !important;
        border: 2px solid gray !important;
        color: {haken_icon_farbe} !important;
        border-radius: 6px !important;
        width: 36px !important;
        height: 36px !important;
    }}
    .st-key-kreuz_{i} button {{
        background-color: {kreuz_farbe} !important;
        border: 2px solid gray !important;
        color: {kreuz_icon_farbe} !important;
        border-radius: 6px !important;
        width: 36px !important;
        height: 36px !important;
    }}
    """

    with col1:
        with st.container(key=f"haken_{i}"):
            if st.button("✓", key=f"btn_haken_{i}"):
                aufgabe["erledigt"] = True
                speichern()
                st.rerun()

    with col2:
        with st.container(key=f"kreuz_{i}"):
            if st.button("✗", key=f"btn_kreuz_{i}"):
                aufgabe["erledigt"] = False
                speichern()
                st.rerun()

    with col3:
        if st.button("🗑", key=f"delete_{i}"):
            zu_loeschen = i

    st.write("")

st.markdown(f"<style>{css_regeln}</style>", unsafe_allow_html=True)

if zu_loeschen is not None:
    st.session_state.aufgaben.pop(zu_loeschen)
    speichern()
    st.rerun()