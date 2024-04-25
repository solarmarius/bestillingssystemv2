"""
Displays the varetelling page
"""

import datetime

import streamlit as st
import pandas as pd

from utils.data import create_smais, create_multipack, create_dessert, combine_data
from utils.email import send_email
from utils.display import menu
from utils.enums import Mode, Operation, BILER

menu()

st.header("Varetelling")

bil = st.selectbox("Bil:", BILER, key="bil", placeholder="Velg bil", index=None)

navn = st.text_input("Sjåfør navn:", key="name", placeholder="Ditt navn")

dato = st.date_input(
    "Tellet:",
    key="dato",
    format="DD/MM/YYYY",
    value=datetime.date.today(),
)
dato = dato.strftime("%d.%m.%Y")

st.header("Telling i bilen", divider="gray")

st.subheader("Småis")
smais_bil = create_smais(keyname="smais_bil", mode=Mode.DISPLAY_FPAKK)

st.subheader("Multipacks")
multipack_bil = create_multipack(keyname="multipack_bil", mode=Mode.DISPLAY_FPAKK)

st.subheader("Desserter")
dessert_bil = create_dessert(keyname="dessert_bil", mode=Mode.DISPLAY_FPAKK)

st.header("Telling på fryser", divider="gray")

st.subheader("Småis")
smais_fryser = create_smais(keyname="smais_fryser", mode=Mode.DISPLAY_FPAKK)

st.subheader("Multipacks")
multipack_fryser = create_multipack(keyname="multipack_fryser", mode=Mode.DISPLAY_FPAKK)

st.subheader("Desserter")
dessert_fryser = create_dessert(keyname="dessert_fryser", mode=Mode.DISPLAY_FPAKK)

st.write(f"Er du ferdig å telle?:")
summer = st.button("Summer telling", type="primary", use_container_width=True)
if summer:
    bestilling_smais = combine_data(smais_bil, smais_fryser)
    bestilling_smais = bestilling_smais.loc[
        (bestilling_smais["Antalldpakk"] != 0) | (bestilling_smais["Antallfpakk"] != 0)
    ]
    bestilling_multipack = combine_data(multipack_bil, multipack_fryser)
    bestilling_multipack = bestilling_multipack.loc[
        (bestilling_multipack["Antalldpakk"] != 0)
        | (bestilling_multipack["Antallfpakk"] != 0)
    ]
    bestilling_dessert = combine_data(dessert_bil, dessert_fryser)
    bestilling_dessert = bestilling_dessert.loc[
        (bestilling_dessert["Antalldpakk"] != 0)
        | (bestilling_dessert["Antallfpakk"] != 0)
    ]

    st.write("Du har tellt (dobbelsjekk!)")
    if "bestilling" not in st.session_state:
        st.session_state["bestilling"] = pd.concat(
            [bestilling_smais, bestilling_multipack, bestilling_dessert]
        )
    else:
        st.session_state["bestilling"] = pd.concat(
            [bestilling_smais, bestilling_multipack, bestilling_dessert]
        )
    st.dataframe(
        st.session_state.bestilling[["Artikkelnavn", "Antalldpakk", "Antallfpakk"]],
        hide_index=True,
        use_container_width=True,
    )

st.write("Er det noen flere iser som ikke står på lista? Skriv under på formen")
st.write("*NAVN PÅ ISEN - ANTALL D-PAKK - ANTALL F-PAKK*")
flere_iser = st.text_area(label="flereiser", label_visibility="hidden")


with st.form(key="bestillingsform_vrak", border=False):
    if bil == None or navn == "" or not summer:
        st.write(
            "Bil / dato / navn må være fyllt ut, eller du må klikke summeringsknappen!"
        )
        submitted = st.form_submit_button(
            "Send inn", use_container_width=True, type="primary", disabled=True
        )
    else:
        submitted = st.form_submit_button(
            "Send inn", use_container_width=True, type="primary"
        )

    if submitted:
        with st.spinner("Sender varetelling..."):
            success = send_email(
                bilfra=bil,
                biltil=None,
                dato=dato,
                person=navn,
                selgernummer=None,
                bestilling=st.session_state.bestilling,
                mode=Operation.VARETELLING,
                arsak=None,
                flereiser=flere_iser,
            )
        if success:
            st.success(
                "Varetelling sendt inn for {}, av {}, den {}".format(bil, navn, dato)
            )
            st.write("Du kan nå lukke appen.")
        else:
            st.error("Vennligst prøv igjen.")
