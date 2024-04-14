"""
Displays the vrak tab.
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

st.header("Vrakordre")

bil = st.selectbox("Bil:", ("790", "791", "792"), key="bil", placeholder="Velg bil", index=None)

navn = st.text_input("Sjåfør navn:", key="name_vrak", placeholder="Ditt navn")

dato = st.date_input("Vraket dato:", key="dato", format="DD/MM/YYYY", value=datetime.date.today()+datetime.timedelta(days=1))
dato = dato.strftime("%d.%m.%Y")

st.subheader("Småis")
smais = create_smais()

st.subheader("Multipacks")
multipack = create_multipack()

st.subheader("Desserter")
dessert = create_dessert()

arsak = st.text_input("Årsak:", key="arsak", placeholder="Hva er årsaken til å vrake isen?")

st.write("Du skal bestille (dobbelsjekk!)")
bestilling_smais = smais.loc[smais["Antalldpakk"] != 0]
bestilling_multipack = multipack.loc[multipack["Antalldpakk"] != 0]
bestilling_dessert = dessert.loc[dessert["Antalldpakk"] != 0]

bestilling = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
st.dataframe(bestilling[["Artikkelnavn", "Antalldpakk"]], hide_index=True, use_container_width=True)

with st.form(key="bestillingsform_vrak", border=False):
    if bil == None or navn == "" or arsak == "":
        st.write("Bil / dato / navn / årsak må være fyllt ut!")
        submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary", disabled=True)
    else:
        submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary")
        
    if submitted:
        with st.spinner("Sender bestilling..."):
            send_email(bilfra=bil, 
                    biltil=None, 
                    dato=dato, 
                    person=navn, 
                    selgernummer=None, 
                    bestilling=bestilling, 
                    arsak=arsak, 
                    mode=4)
        st.success("Vrakordre sendt inn for {}, av {}, den {}".format(bil, navn, dato))
        st.write("Du kan nå lukke appen.")