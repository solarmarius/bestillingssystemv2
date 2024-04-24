"""
Displays the varebestilling tab.
"""

from data import create_smais
from data import create_multipack
from data import create_dessert

from utils import send_email
from utils import menu

import streamlit as st
import pandas as pd
import datetime

menu()

st.header("Varebestilling")

# Inputs
bil_bes = st.selectbox(
    "Bil:", ("790", "791", "792"), key="bil_bes", placeholder="Velg bil", index=None
)

navn_bes = st.text_input("Sjåfør navn:", key="name_bes", placeholder="Ditt navn")

dato_bes = st.date_input(
    "Bestilt til dato:",
    key="dato_bes",
    format="DD/MM/YYYY",
    value=datetime.date.today() + datetime.timedelta(days=1),
)
dato_bes = dato_bes.strftime("%d.%m.%Y")

st.subheader("Småis")
smais = create_smais(keyname="smais")

st.subheader("Multipacks")
multipack = create_multipack(keyname="multipack")

st.subheader("Desserter")
dessert = create_dessert(keyname="dessert")

st.write("Du skal bestille (dobbelsjekk!)")
bestilling_smais = smais.loc[smais["Antalldpakk"] != 0]
bestilling_multipack = multipack.loc[multipack["Antalldpakk"] != 0]
bestilling_dessert = dessert.loc[dessert["Antalldpakk"] != 0]

bestilling = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
st.dataframe(
    bestilling[["Artikkelnavn", "Antalldpakk"]],
    hide_index=True,
    use_container_width=True,
)

with st.form(key="bestillingsform_bes", border=False):
    if bil_bes == None or navn_bes == "":
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
            send_email(
                bilfra=bil_bes,
                biltil=None,
                dato=dato_bes,
                person=navn_bes,
                selgernummer=None,
                bestilling=bestilling,
                arsak=None,
                mode=1,
            )
        st.success(
            "Bestilling sendt inn for {}, av {}, den {}".format(
                bil_bes, navn_bes, dato_bes
            )
        )
        st.write("Du kan nå lukke appen.")
