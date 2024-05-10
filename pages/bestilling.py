"""
Displays the varebestilling tab.
"""

import datetime

import streamlit as st
import pandas as pd

from utils.data import create_smais, create_multipack, create_dessert
from utils.email import send_email
from utils.display import menu
from utils.enums import Mode, Operation, BILER

menu()

st.header("Varebestilling")

# Inputs
bil = st.selectbox("Bil:", BILER, key="bil", placeholder="Velg bil", index=None)

navn = st.text_input("Sjåfør navn:", key="name_bes", placeholder="Ditt navn")

dato = st.date_input(
    "Bestilt til dato:",
    key="dato",
    format="DD/MM/YYYY",
    value=datetime.date.today() + datetime.timedelta(days=1),
)
dato = dato.strftime("%d.%m.%Y")

st.subheader("Småis")
smais = create_smais(keyname="smais", mode=Mode.DEFAULT)

st.subheader("Multipacks")
multipack = create_multipack(keyname="multipack", mode=Mode.DEFAULT)

st.subheader("Desserter")
dessert = create_dessert(keyname="dessert", mode=Mode.DEFAULT)

st.write("Du skal bestille (dobbelsjekk!)")
bestilling_smais = smais.loc[smais["Antalldpakk"] > 0]
bestilling_multipack = multipack.loc[multipack["Antalldpakk"] > 0]
bestilling_dessert = dessert.loc[dessert["Antalldpakk"] > 0]

bestilling = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
st.dataframe(
    bestilling[["Artikkelnavn", "Antalldpakk"]],
    hide_index=True,
    use_container_width=True,
)

with st.form(key="bestillingsform_bes", border=False):
    if bil == None or navn == "":
        st.write("Bil / navn / dato må være fyllt ut!")
        submitted = st.form_submit_button(
            "Send inn", use_container_width=True, type="primary", disabled=True
        )
    else:
        submitted = st.form_submit_button(
            "Send inn", use_container_width=True, type="primary"
        )

    if submitted:
        with st.spinner("Sender bestilling..."):
            success = send_email(
                bilfra=bil,
                biltil=None,
                dato=dato,
                person=navn,
                selgernummer=None,
                bestilling=bestilling,
                arsak=None,
                mode=Operation.BESTILLING,
            )
        if success:
            st.success(
                "Bestilling sendt inn for {}, av {}, den {}".format(bil, navn, dato)
            )
            st.write("Du kan nå lukke appen.")
        else:
            st.error("Vennligst prøv igjen.")
