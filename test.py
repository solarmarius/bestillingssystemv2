import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)
authenticator.login()

if st.session_state["authentication_status"]:
    st.switch_page("pages/admin.py")
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

