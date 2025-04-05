import streamlit as st
from gui.utils import load_css, create_sidebar

def show():
    # Load CSS
    load_css()
    
    # Create sidebar
    create_sidebar()
    
    # Main content
    st.title("Page Title")  # Jeweils der entsprechende Titel
    st.write("Under construction")  # Platzhalter

if __name__ == "__main__":
    show()