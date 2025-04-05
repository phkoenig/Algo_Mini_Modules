import streamlit as st
from gui.utils import load_css

def show():
    # Lade das CSS für einheitliches Styling
    load_css()
    
    st.title("9. Live Trading")
    st.write("Live Trading-Seite im Aufbau")

# Wenn die Datei direkt ausgeführt wird
if __name__ == "__main__":
    show() 