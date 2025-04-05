import streamlit as st
from gui.utils import load_css
from gui.components.sidebar import create_sidebar

# Erlaubte Emails aus README_Google_Auth.md
ALLOWED_EMAILS = [
    "phkoenig@gmail.com",
    "philip@zepta.com", 
    "carmenkoenig2412@gmail.com",
    "karlvictorkoenig@gmail.com"
]

def main():
    load_css()  # Nutzt existierendes CSS aus static/css
    
    st.title("🔐 Login")
    
    # Simple Login-Logik
    if not st.experimental_user.is_logged_in:  # Removed the parentheses
        if st.button("🔑 Mit Google einloggen"):
            st.login("google")
    elif st.experimental_user.email in ALLOWED_EMAILS:
        create_sidebar()  # Nutzt existierende Sidebar-Komponente
        st.success(f"Willkommen, {st.experimental_user.name}!")
        if st.button("🚪 Ausloggen"): 
            st.logout()
    else:
        st.error("E-Mail nicht berechtigt")
        st.button("↩️ Zurück", on_click=st.logout)

if __name__ == "__main__":
    main()