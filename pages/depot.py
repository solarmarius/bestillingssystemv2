"""
Page where the administrator can change the
logins for depotene
"""

import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth


with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)
authenticator.login()

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"### Velkommen, {st.session_state['name']}")
    with col2:
        if st.button(label="⏪ Tilbake", use_container_width=True):
            st.switch_page("pages/admin.py")

st.write("Du er kul")
