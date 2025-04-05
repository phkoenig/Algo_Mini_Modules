import streamlit as st
from gui.utils import load_css

# Seitenkonfiguration
st.set_page_config(
    page_title="1_Login",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Lade das CSS für einheitliches Styling
load_css()

# Hauptbereich
st.title("Login")
st.write("Bitte melde dich an, um die Plattform zu nutzen.")