"""
Displays the vareoverføring tab.
"""

import datetime

import streamlit as st
import pandas as pd

from utils.data import create_smais, create_multipack, create_dessert
from utils.email import send_email
from utils.display import menu
from utils.enums import Mode, Operation, BILER

menu()

# display_overforing(bilfra_input, biltil_input, navn_input, dato_input)
st.header("Vareoverføring")

bilfra = st.selectbox(
    "Bil:", BILER, key="bilfra", placeholder="Velg bil fra", index=None
)
biltil = st.selectbox(
    "Bil:", BILER, key="biltil", placeholder="Velg bil til", index=None
)

if (bilfra != None or biltil != None) and (bilfra == biltil):
    st.error("Bil fra / bil til er det samme!")

navn = st.text_input("Sjåfør navn:", key="name", placeholder="Ditt navn")

dato = st.date_input(
    "Overført dato:", key="dato", format="DD/MM/YYYY", value=datetime.date.today()
)
dato = dato.strftime("%d.%m.%Y")

st.subheader("Småis")
smais = create_smais(keyname="smais", mode=Mode.DEFAULT)

st.subheader("Multipacks")
multipack = create_multipack(keyname="multipack", mode=Mode.DEFAULT)

st.subheader("Desserter")
dessert = create_dessert(keyname="dessert", mode=Mode.DEFAULT)

st.write(f"Du skal overføre fra {bilfra} til {biltil} (dobbelsjekk!):")
bestilling_smais = smais.loc[smais["Antalldpakk"] != 0]
bestilling_multipack = multipack.loc[multipack["Antalldpakk"] != 0]
bestilling_dessert = dessert.loc[dessert["Antalldpakk"] != 0]

bestilling = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
st.dataframe(
    bestilling[["Artikkelnavn", "Antalldpakk"]],
    hide_index=True,
    use_container_width=True,
)

with st.form(key="bestillingsform_ov", border=False):

    if bilfra == None or biltil == None or navn == "":
        st.write("Bil / dato / navn må være fyllt ut!")
        submitted = st.form_submit_button(
            "Send inn", use_container_width=True, type="primary", disabled=True
        )
    else:
        submitted = st.form_submit_button(
            "Send inn", use_container_width=True, type="primary"
        )

    if submitted:
        with st.spinner("Sender overføring..."):
            success = send_email(
                bilfra=bilfra,
                biltil=biltil,
                dato=dato,
                person=navn,
                selgernummer=None,
                bestilling=bestilling,
                arsak=None,
                mode=Operation.OVERFORING,
            )
        if success:
            st.success(
                "Overføring sendt inn fra bil {}, til bil {}, den {}".format(
                    bilfra, biltil, dato
                )
            )
            st.write("Du kan nå lukke appen.")
        else:
            st.error("Vennligst prøv igjen.")
