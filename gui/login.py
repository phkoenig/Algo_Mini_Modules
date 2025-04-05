import streamlit as st
from gui.utils import load_css, create_sidebar

def main():
    # Page config
    st.set_page_config(
        page_title="Algo Trading Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load CSS
    load_css()
    
    # Create sidebar
    create_sidebar()
    
    # Main content
    st.title("Welcome")
    st.write("Welcome to the Algo Trading Dashboard")

if __name__ == "__main__":
    main()