"""
Utility-Funktionen für die Streamlit GUI
"""

import pathlib
import streamlit as st

def load_css():
    """Lädt das zentrale CSS-Styling für alle Pages"""
    css_file = pathlib.Path("gui/static/css/style.css").read_text()
    st.markdown(f"<style>{css_file}</style>", unsafe_allow_html=True) 