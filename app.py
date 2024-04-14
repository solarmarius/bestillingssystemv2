"""
Main app.
"""

import streamlit as st
import hmac

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    img, head = st.columns(spec=[0.2,0.8], gap="small")
    with img:
        st.image("images/logo.png", width=100)
    with head:
        st.header("Velkommen til bestillingsportalen :icecream:", divider="orange")
        
    st.text_input(
        "Kode, (for Tromsø: inngangskode til kontor):", on_change=password_entered, key="password", placeholder="4-sifret tall (trykk enter)"
    )
    if "password_correct" in st.session_state:
        st.error("Vennligst skriv inn korrekt kode")
    return False

# No access to interface before correct password
if not check_password():
    st.stop()

# If correct, redirect to "default" page -> Varebestilling
st.switch_page("pages/bestilling.py")