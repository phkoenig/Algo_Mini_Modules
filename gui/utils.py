"""
Utility-Funktionen für die Streamlit GUI
"""

import pathlib
import streamlit as st
from .components.sidebar import create_sidebar

def load_css():
    """Load custom CSS styles"""
    with open("gui/static/css/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

__all__ = ['load_css', 'create_sidebar'] 