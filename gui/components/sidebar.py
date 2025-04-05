"""
Zentrale Sidebar-Komponente für die Streamlit GUI
"""

import streamlit as st

def create_sidebar():
    """Erstellt und verwaltet die zentrale Sidebar für alle Pages"""
    
    # Footer mit Versionsnummer am unteren Rand
    st.sidebar.markdown(
        '<div style="text-align: center; color: #666666; font-size: 0.8em;">'
        'Version 1.0.0'
        '</div>',
        unsafe_allow_html=True
    )
