"""
Page where the administrator can change the
iskrems
"""

import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd


def change_csv(
    smais: pd.DataFrame, multipack: pd.DataFrame, desserter: pd.DataFrame
) -> None:
    """
    Writes to the csv files (data) with updated entries.
    """
    # Make sure that all entries are zeroed out (int)
    smais = smais.assign(Antalldpakk=0, Antallfpakk=0)
    smais.to_csv("data/testsmais.csv", index=False, sep=";")

    multipack = multipack.assign(Antalldpakk=0, Antallfpakk=0)
    multipack.to_csv("data/testmultipack.csv", index=False, sep=";")

    desserter = desserter.assign(Antalldpakk=0, Antallfpakk=0)
    desserter.to_csv("data/testdesserter.csv", index=False, sep=";")


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

st.header("Endre isene")
st.write(
    "Her kan du endre isene. Dette gjør du ved å modifisere verdiene i tabellene, så lagre."
)

smais_data = pd.read_csv("data/smais.csv", sep=";", converters={"Artikkelnummer": str})
multipack_data = pd.read_csv(
    "data/multipacks.csv", sep=";", converters={"Artikkelnummer": str}
)
desserter_data = pd.read_csv(
    "data/dessert.csv", sep=";", converters={"Artikkelnummer": str}
)

st.subheader("Småis")
smais = st.data_editor(
    smais_data,
    hide_index=True,
    use_container_width=True,
    key="smais",
    column_order=("Artikkelnummer", "Artikkelnavn"),
    num_rows="dynamic",
)
if ((smais["Artikkelnummer"].str.len() != 5).any()) > 0:
    st.error("Ser ut som et artikkelnummer i tabellen ikke er 5-sifferet!")

st.subheader("Multipacks")
multipack = st.data_editor(
    multipack_data,
    hide_index=True,
    use_container_width=True,
    key="multipack",
    column_order=("Artikkelnummer", "Artikkelnavn"),
    num_rows="dynamic",
)
if ((multipack["Artikkelnummer"].str.len() != 5).any()) > 0:
    st.error("Ser ut som et artikkelnummer i tabellen ikke er 5-sifferet!")

st.subheader("Desserter")
desserter = st.data_editor(
    desserter_data,
    hide_index=True,
    use_container_width=True,
    key="desserter",
    column_order=("Artikkelnummer", "Artikkelnavn"),
    num_rows="dynamic",
)
if ((desserter["Artikkelnummer"].str.len() != 5).any()) > 0:
    st.error("Ser ut som et artikkelnummer i tabellen ikke er 5-sifferet!")

if st.button("Lagre", use_container_width=True, type="primary"):
    with st.spinner("Lagrer endringer..."):
        change_csv(smais, multipack, desserter)
    st.success("Endringene er nå lagret!")
