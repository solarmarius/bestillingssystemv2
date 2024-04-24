"""
Interface for admin (markedsansvarlig) bruker. 
Can change the data that is displayed in the main interface (add ice creams, remove etc)
"""

import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth


def display_admin():
    """
    Displays the admin interface.
    """
    with st.container(border=True):
        st.write(f"### Velkommen, {st.session_state['name']}")
        authenticator.logout(button_name="Logg ut")

    st.header("Du kan gjøre følgende:")
    if st.button(
        label="Legg til/endre isene", use_container_width=True, type="primary"
    ):
        st.switch_page("pages/endre.py")
    if st.button(
        label="Legg til/endre innlogg for depotene",
        use_container_width=True,
        type="primary",
    ):
        st.switch_page("pages/depot.py")


with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Authenticator interface
authenticator.login(
    fields={
        "Form name": "Logg inn for adminstrator",
        "Username": "Brukernavn",
        "Password": "Passord",
        "Login": "Logg inn",
    }
)
if st.session_state["authentication_status"]:
    display_admin()
elif st.session_state["authentication_status"] is False:
    st.error("Brukernavn / passord er feil!")
    if st.button(label="⏪ Tilbake", use_container_width=True):
        st.switch_page("./app.py")
elif st.session_state["authentication_status"] is None:
    if st.button(label="⏪ Tilbake", use_container_width=True):
        st.switch_page("./app.py")
