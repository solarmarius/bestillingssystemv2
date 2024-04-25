"""
Displays the personalbestilling tab.
"""

import datetime

import streamlit as st
import pandas as pd

from utils.data import create_smais, create_multipack, create_dessert
from utils.email import send_email
from utils.display import menu
from utils.enums import Mode, Operation

menu()

st.header("Personalbestilling")

navn = st.text_input("Sjåfør navn:", key="name_per", placeholder="Ditt navn")
nummer = st.text_input("Selgernummer:", key="nummer", placeholder="Ditt selgernummer")

dato = st.date_input(
    "Bestillt til dato:",
    key="dato",
    format="DD/MM/YYYY",
    value=datetime.date.today() + datetime.timedelta(days=1),
)
dato = dato.strftime("%d.%m.%Y")

st.write("NB: Du bestiller D-pakk. Merk antall på isene, spesielt på multipacks!")

st.subheader("Småis")
smais = create_smais(keyname="smais", mode=Mode.DEFAULT)

st.subheader("Multipacks")
multipack = create_multipack(keyname="multipack", mode=Mode.DEFAULT)

st.subheader("Desserter")
dessert = create_dessert(keyname="dessert", mode=Mode.DEFAULT)

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

with st.form(key="bestillingsform_per", border=False):

    if navn == "" or nummer == "":
        st.write("Navn / selgernummer / dato må være fyllt ut!")
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
                bilfra=None,
                biltil=None,
                dato=dato,
                person=navn,
                selgernummer=nummer,
                bestilling=bestilling,
                arsak=None,
                mode=Operation.PERSONAL,
            )
        if success:
            st.success("Personalbestilling sendt inn for {} den {}".format(navn, dato))
            st.write("Du kan nå lukke appen.")
        else:
            st.error("Vennligst prøv igjen.")
