"""
Displays the vareoverføring tab.
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

# display_overforing(bilfra_input, biltil_input, navn_input, dato_input)
st.header("Vareoverføring")

bilfra = st.selectbox("Bil:", ("790", "791", "792"), key="bilfra", placeholder="Velg bil fra", index=None)
biltil = st.selectbox("Bil:", ("790", "791", "792"), key="biltil", placeholder="Velg bil til", index=None)

if (bilfra != None or biltil != None) and (bilfra == biltil):
    st.error("Bil fra / bil til er det samme!")

navn = st.text_input("Sjåfør navn:", key="name", placeholder="Ditt navn")

dato = st.date_input("Overført dato:", key="dato", format="DD/MM/YYYY", value=datetime.date.today()+datetime.timedelta(days=1))
dato = dato.strftime("%d.%m.%Y")

st.subheader("Småis")
smais = create_smais()

st.subheader("Multipacks")
multipack = create_multipack()

st.subheader("Desserter")
dessert = create_dessert()

st.write("Du skal bestille (dobbelsjekk!)")
bestilling_smais = smais.loc[smais["Antalldpakk"] != 0]
bestilling_multipack = multipack.loc[multipack["Antalldpakk"] != 0]
bestilling_dessert = dessert.loc[dessert["Antalldpakk"] != 0]

bestilling = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
st.dataframe(bestilling[["Artikkelnavn", "Antalldpakk"]], hide_index=True, use_container_width=True)

with st.form(key="bestillingsform_ov", border=False):
    
    if bilfra == None or biltil == None or navn == "":
        st.write("Bil / dato / navn må være fyllt ut!")
        submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary", disabled=True)
    else:
        submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary")
        
    if submitted:
        with st.spinner("Sender bestilling..."):
            send_email(bilfra=bilfra, 
                    biltil=biltil,
                    dato=dato, 
                    person=navn, 
                    selgernummer=None, 
                    bestilling=bestilling, 
                    arsak=None, 
                    mode=2)
        st.success("Overføring sendt inn fra bil {}, til bil {}, den {}".format(bilfra, biltil, dato))
        st.write("Du kan nå lukke appen.")