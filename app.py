from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st
import pandas as pd
import datetime
import smtplib
import hmac

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Kode (trykk enter)", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("Vennligst skriv inn korrekt kode")
    return False

def send_email(bil, dato, person, bestilling):
    print(bestilling)
    
    message = MIMEMultipart()
    message["Subject"] = "Varebestilling fra Tromsø"
    message["From"] = st.secrets["SENDER_ADDRESS"]
    message["To"] = st.secrets["RECEIVER_ADDRESS"]
    message.attach(MIMEText("Bil: {} \nBestilt til dato: {}\nSjåfør navn: {}\n\nBestilling gjelder:\n{}".format(bil, dato, person, bestilling)))

    
    server = smtplib.SMTP(st.secrets["SMTP_SERVER_ADDRESS"], st.secrets["PORT"])
    server.starttls()
    server.ehlo()
    server.login(st.secrets["SENDER_ADDRESS"], st.secrets["SENDER_PASSWORD"])
    text = message.as_string()
    
    server.sendmail(st.secrets["SENDER_ADDRESS"], st.secrets["RECEIVER_ADDRESS"], text)
    server.quit()

if not check_password():
    st.stop()

smais = pd.read_csv("bestllingslistecsvv2.csv", sep=";", nrows=31, converters={'Artikkelnummer': str})
multipack = pd.read_csv("bestllingslistecsvv2.csv", sep=";", skiprows=[i for i in range(1, 32)], nrows=29, converters={'Artikkelnummer': str})
dessert = pd.read_csv("bestllingslistecsvv2.csv", sep=";", skiprows=[i for i in range(1, 61)], converters={'Artikkelnummer': str})

st.header("Varebestilling for Tromsø")

bil = st.selectbox("Bil:", ("790", "791", "792"), key="bil", placeholder="Velg bil", index=None)

navn = st.text_input("Sjåfør navn:", key="name", placeholder="Ditt navn")

dato = st.date_input("Bestilt til dato:", key="dato", format="DD/MM/YYYY", value=datetime.date.today()+datetime.timedelta(days=1))
dato = dato.strftime("%d/%m/%Y")


st.write("Småis")
edit_smais = st.data_editor(smais, hide_index=True, use_container_width=True, disabled=(1, 2), 
                            column_config={
                                "Antalldpakk": st.column_config.NumberColumn(
                                    "Antall D-pakk",
                                    min_value = 0,
                                    max_value = 16,
                                    step=1
                                ),
                                "Artikkelnummer": None
                            })

st.write("Multipacks")
edit_multipack = st.data_editor(multipack, hide_index=True, use_container_width=True, disabled=(1, 2),
                                column_config={
                                    "Antalldpakk": st.column_config.NumberColumn(
                                        "Antall D-pakk",
                                        min_value = 0,
                                        max_value = 16,
                                        step=1
                                    )
                            })

st.write("Desserter")
edit_dessert = st.data_editor(dessert, hide_index=True, use_container_width=True, disabled=(1, 2),
                            column_config={
                                "Antalldpakk": st.column_config.NumberColumn(
                                    "Antall D-pakk",
                                    min_value = 0,
                                    max_value = 16,
                                    step=1)
                            })

st.write("Du skal bestille (dobbelsjekk!)")
bestilling_smais = edit_smais.loc[edit_smais["Antalldpakk"] != 0]
bestilling_multipack = edit_multipack.loc[edit_multipack["Antalldpakk"] != 0]
bestilling_dessert = edit_dessert.loc[edit_dessert["Antalldpakk"] != 0]

bestilling = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
st.data_editor(bestilling, use_container_width=True, hide_index=True, disabled=True)

bestilling_email = ""

with st.form(key="bestillingsform", border=False):
    
    for rad in bestilling.index:
        artnr = bestilling["Artikkelnummer"][rad]
        artnavn = bestilling["Artikkelnavn"][rad]
        antalldpakk = bestilling["Antalldpakk"][rad]
        bestilling_email += "{} | {} | {}\n".format(artnr, artnavn, antalldpakk)
    
    if (bil == None or navn == None or dato == None):
        st.write("Bil / dato / navn må være fyllt ut!")
        submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary", disabled=True)
    else:
        submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary")
        
    if submitted:
        send_email(bil, dato, navn, bestilling_email)
        st.write("Bestilling sendt inn for {}, {}, {}".format(bil, navn, dato))
        st.write("Du kan nå lukke appen.")