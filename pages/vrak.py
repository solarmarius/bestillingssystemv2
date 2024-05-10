"""
Displays the vrak tab.
"""

import datetime

import streamlit as st
import pandas as pd

from utils.data import create_smais, create_multipack, create_dessert
from utils.email import send_email
from utils.display import menu
from utils.enums import Mode, Operation, BILER

menu()

st.header("Vrakordre")

bil = st.selectbox("Bil:", BILER, key="bil", placeholder="Velg bil", index=None)

navn = st.text_input("Sjåfør navn:", key="name_vrak", placeholder="Ditt navn")

dato = st.date_input(
    "Vraket dato:",
    key="dato",
    format="DD/MM/YYYY",
    value=datetime.date.today(),
)
dato = dato.strftime("%d.%m.%Y")

st.subheader("Småis")
smais = create_smais(keyname="smais", mode=Mode.DISPLAY_FPAKK)

st.subheader("Multipacks")
multipack = create_multipack(keyname="multipack", mode=Mode.DISPLAY_FPAKK)

st.subheader("Desserter")
dessert = create_dessert(keyname="dessert", mode=Mode.DISPLAY_FPAKK)

arsak = st.text_input(
    "Årsak:", key="arsak", placeholder="Hva er årsaken til å vrake isen?"
)

st.write(f"Du skal vrake på grunn av {arsak} (dobbelsjekk!):")
bestilling_smais = smais.loc[(smais["Antalldpakk"] > 0) | (smais["Antallfpakk"] > 0)]
bestilling_multipack = multipack.loc[
    (multipack["Antalldpakk"] > 0) | (multipack["Antallfpakk"] > 0)
]
bestilling_dessert = dessert.loc[
    (dessert["Antalldpakk"] > 0) | (dessert["Antallfpakk"] > 0)
]

bestilling = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
st.dataframe(
    bestilling[["Artikkelnavn", "Antalldpakk", "Antallfpakk"]],
    hide_index=True,
    use_container_width=True,
)

with st.form(key="bestillingsform_vrak", border=False):
    if bil == None or navn == "" or arsak == "":
        st.write("Bil / dato / navn / årsak må være fyllt ut!")
        submitted = st.form_submit_button(
            "Send inn", use_container_width=True, type="primary", disabled=True
        )
    else:
        submitted = st.form_submit_button(
            "Send inn", use_container_width=True, type="primary"
        )

    if submitted:
        with st.spinner("Sender vrakordre..."):
            success = send_email(
                bilfra=bil,
                biltil=None,
                dato=dato,
                person=navn,
                selgernummer=None,
                bestilling=bestilling,
                arsak=arsak,
                mode=Operation.VRAKORDRE,
            )
        if success:
            st.success(
                "Vrakordre sendt inn for {}, av {}, den {}".format(bil, navn, dato)
            )
            st.write("Du kan nå lukke appen.")
        else:
            st.error("Vennligst prøv igjen.")
