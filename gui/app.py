import streamlit as st

# Seitenkonfiguration
st.set_page_config(
    page_title="1_Login",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Lade das externe CSS
css_file = pathlib.Path("gui/static/css/style.css").read_text()
st.markdown(f"<style>{css_file}</style>", unsafe_allow_html=True)

# Hauptbereich
st.title("Login")
st.write("Bitte melde dich an, um die Plattform zu nutzen.")

# Login-Formular
with st.form("login_form"):
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")
    submitted = st.form_submit_button("Anmelden")
    
    if submitted:
        st.info("Login-Funktionalität wird implementiert...")

# Version Footer
st.sidebar.markdown("---")
st.sidebar.markdown("v0.1.0") 