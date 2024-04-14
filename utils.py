"""
Utility functions, check password and send email
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st
import pandas as pd
import smtplib
import hmac

def send_email(bilfra, biltil, dato, person, selgernummer, bestilling:pd.DataFrame, arsak, mode):
    """Sends email to a specified address (lager)"""
    bestilling_string = ""
    
    # Reset index, sometimes the index resets after 20 items
    bestilling = bestilling.reset_index()
    
    for rad in bestilling.index:
        artnr = str(bestilling["Artikkelnummer"][rad])
        artnavn = str(bestilling["Artikkelnavn"][rad])
        antalldpakk = str(bestilling["Antalldpakk"][rad])
        bes = "{} | {} | {}\n".format(artnr, artnavn, antalldpakk)
        bestilling_string += bes
    
    message = MIMEMultipart()
    message["Subject"] = "Bestilling fra Tromsø {}".format(dato)
    message["From"] = st.secrets["SENDER_ADDRESS"]
    message["To"] = st.secrets["RECEIVER_ADDRESS"]
    if mode == 1: # Varebestilling
        message.attach(MIMEText("VAREBESTILLING\nBil: {} \nBestilt til dato: {}\nSjåfør navn: {}\n\nBestilling gjelder:\n{}".format(bilfra, dato, person, bestilling_string)))
    if mode == 2: # Vareoverføring
        message.attach(MIMEText("VAREOVERFØRING\nBil fra: {} \nBil til: {} \nOverført dato: {}\nSjåfør navn: {}\n\nOverføringen gjelder:\n{}".format(bilfra, biltil, dato, person, bestilling_string)))
    if mode == 3: # Personalbestilling
        message.attach(MIMEText("PERSONALBESTILLING\nSelgernummer: {} \nBestilt til dato: {}\nSjåfør navn: {}\n\nPersonalbestilling gjelder:\n{}".format(selgernummer, dato, person, bestilling_string)))
    if mode == 4: # Vrakordre
        message.attach(MIMEText("VRAKORDRE\nBil: {} \nVraket dato: {}\nSjåfør navn: {}\nÅrsak: {}\n\nVrakordre gjelder:\n{}".format(bilfra, dato, person, arsak, bestilling_string)))  

    
    server = smtplib.SMTP(st.secrets["SMTP_SERVER_ADDRESS"], st.secrets["PORT"])
    server.starttls()
    server.ehlo()
    server.login(st.secrets["SENDER_ADDRESS"], st.secrets["SENDER_PASSWORD"])
    text = message.as_string()
    
    server.sendmail(st.secrets["SENDER_ADDRESS"], st.secrets["RECEIVER_ADDRESS"], text)
    server.quit()
    
def create_bestilling_string(data: pd.DataFrame)->str:
    """ 
    From a dataframe (order), create a string to be parsed to an email
    """
    bestilling_email = ""
    
    for rad in data.index:
        artnr = str(data["Artikkelnummer"][rad])
        artnavn = str(data["Artikkelnavn"][rad])
        antalldpakk = str(data["Antalldpakk"][rad])
        bes = "{} | {} | {}\n".format(artnr, artnavn, antalldpakk)
        bestilling_email += bes
    
    return bestilling_email

def menu():
    """
    Shows the menu
    """
    ### MAIN INTERFACE ###
    st.header("Bestillingsportal for Tromsø")

    # Menu
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.page_link("pages/bestilling.py", label="Varebestilling", icon="📬")

    with col2:
        st.page_link("pages/overforing.py", label="Vareoverføring", icon="↪️")

    with col3:
        st.page_link("pages/personal.py", label="Personalbestilling", icon="💁")

    with col4:
        st.page_link("pages/vrak.py", label="Vrak", icon="🗑️")

    st.divider()