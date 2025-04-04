import streamlit as st

# Liste der erlaubten E-Mail-Adressen
ALLOWED_EMAILS = [
    "philip@koehler.pro",  # Deine E-Mail-Adresse
]

def check_auth():
    """
    Überprüft die Authentifizierung des Benutzers.
    Returns:
        bool: True wenn der Benutzer authentifiziert und berechtigt ist, sonst False
    """
    # Check if user is logged in
    if not st.experimental_user.is_logged_in:
        st.info("Bitte melde dich an, um fortzufahren.")
        if st.button("Mit Google einloggen"):
            st.login("google")
            
        st.write("Erlaubte E-Mail-Adressen:")
        for email in ALLOWED_EMAILS:
            st.write(f"- `{email}`")
        return False
    
    # Check if email is allowed
    if st.experimental_user.email in ALLOWED_EMAILS:
        st.success(f"👋 Willkommen, {st.experimental_user.name}!")
        return True
    else:
        st.error(f"Sorry, die E-Mail-Adresse {st.experimental_user.email} ist nicht berechtigt.")
        st.logout()
        return False

def show_user_info():
    """
    Zeigt Benutzerinformationen und Logout-Button an.
    """
    st.sidebar.write("---")
    st.sidebar.write("Login-Informationen:")
    st.sidebar.json({
        "name": st.experimental_user.name,
        "email": st.experimental_user.email
    })
    
    if st.sidebar.button("Ausloggen"):
        st.logout() 