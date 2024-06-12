"""
Utility functions, check password and send email
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils.data import combine_pakk
from utils.enums import Operation
from utils import logger

from collections import namedtuple

import streamlit as st
import pandas as pd
import smtplib
import hmac
import datetime
import numpy as np

Details = namedtuple(
    "Details",
    [
        "bilfra",
        "biltil",
        "dato",
        "person",
        "selgernummer",
        "arsak",
        "bestilling",
        "flereiser",
    ],
)

EMAIL_STRINGS = {
    Operation.BESTILLING: "VAREBESTILLING\nBil: {bilfra} \nBestilt til dato: {dato}\nSjåfør navn: {person}\n\nBestilling gjelder:\n{bestilling}\nEvt. andre varer:\n{flereiser}",
    Operation.OVERFORING: "VAREOVERFØRING\nBil fra: {bilfra} \nBil til: {biltil} \nOverført dato: {dato}\nSjåfør navn: {person}\n\nOverføringen gjelder:\n{bestilling}",
    Operation.PERSONAL: "PERSONALBESTILLING\nSelgernummer: {selgernummer} \nBestilt til dato: {dato}\nSjåfør navn: {person}\n\nPersonalbestilling gjelder:\n{bestilling}",
    Operation.VRAKORDRE: "VRAKORDRE\nBil: {bilfra} \nVraket dato: {dato}\nSjåfør navn: {person}\nÅrsak: {arsak}\n\nVrakordre gjelder: (D-pakk / F-pakk)\n{bestilling}",
    Operation.VARETELLING: "VARETELLING\nBil: {bilfra} \nTelt dato: {dato}\nSjåfør navn: {person}\n\nTelte varer \n{bestilling}\nAndre varer:\n{flereiser}",
}


def create_bestilling_string(
    data: pd.DataFrame, display_fpakk=False, varetelling=False
) -> str:
    """
    From a dataframe (order), create a string to be parsed to an email
    """
    bestilling_string = ""

    for rad in data.index:
        artnr = str(data["Artikkelnummer"][rad])
        artnavn = str(data["Artikkelnavn"][rad])
        antalldpakk = data["Antalldpakk"][rad]
        if display_fpakk:
            antallfpakk = data["Antallfpakk"][rad]
            if np.isnan(antalldpakk):
                antalldpakk = 0.0
            if np.isnan(antallfpakk):
                antallfpakk = 0.0
            line = f"{artnr} | {artnavn} | {antalldpakk:.0f} | {antallfpakk:.0f}\n"
        elif varetelling:
            line = f"{artnr} | {artnavn} | {antalldpakk:.4f}\n"
        else:
            line = f"{artnr} | {artnavn} | {antalldpakk:.0f}\n"
        bestilling_string += line

    return bestilling_string


def send_email(
    bilfra: str,
    biltil: str,
    dato: datetime.date,
    person: str,
    selgernummer: str,
    bestilling: pd.DataFrame,
    arsak: str,
    mode: Operation,
    flereiser=None,
) -> bool:
    """
    Sends email to a specified address (lager).

    Args:
        bilfra (str): The source vehicle.
        biltil (str): The destination vehicle.
        dato (datetime.date): The date of the order.
        person (str): The name of the driver.
        selgernummer (str): The seller number.
        bestilling (pd.DataFrame): The order.
        arsak (str): The reason for the vrakordre.
        mode (Operation): The operation mode.
        flereiser (Optional): Additional ice creams in varetelling.

    Returns:
        None
    """
    bestilling_string = ""

    # Reset index, sometimes the index resets after 20 items
    bestilling = bestilling.reset_index()

    if mode == Operation.VRAKORDRE:
        bestilling_string = create_bestilling_string(bestilling, display_fpakk=True)
    elif mode == Operation.VARETELLING:
        bestilling = combine_pakk(bestilling)
        bestilling_string = create_bestilling_string(bestilling, varetelling=True)
    else:
        bestilling_string = create_bestilling_string(bestilling)

    message = MIMEMultipart()
    message["Subject"] = "Bestilling fra DIB Region Nord {}".format(dato)
    message["From"] = st.secrets["SENDER_ADDRESS"]
    message["To"] = st.secrets["RECEIVER_ADDRESS"]

    details = Details(
        bilfra=bilfra,
        biltil=biltil,
        dato=dato,
        person=person,
        selgernummer=selgernummer,
        arsak=arsak,
        bestilling=bestilling_string,
        flereiser=flereiser,
    )
    message.attach(MIMEText(EMAIL_STRINGS[mode].format(**details._asdict())))
    try:
        server = smtplib.SMTP(st.secrets["SMTP_SERVER_ADDRESS"], st.secrets["PORT"])
    except Exception as e:
        st.error(
            "Kunne ikke koble til server. Sjekk om du er koblet til nett og prøv igjen."
        )
        return False
    server.starttls()
    server.ehlo()
    server.login(st.secrets["SENDER_ADDRESS"], st.secrets["SENDER_PASSWORD"])
    text = message.as_string()

    try:
        if mode == Operation.VARETELLING:
            server.sendmail(
                st.secrets["SENDER_ADDRESS"], st.secrets["VARETELLING_ADDRESS"], text
            )
        else:
            server.sendmail(
                st.secrets["SENDER_ADDRESS"], st.secrets["RECEIVER_ADDRESS"], text
            )
    except Exception as e:
        st.error("Kunne ikke sende mail!")
        logger.error("Exception occurred", exc_info=True)
        server.quit()
        return False

    server.quit()
    return True


if __name__ == "__main__":
    from utils.data import create_dessert
    from datetime import date

    data = create_dessert("test", mode=1)
    send_email(
        bilfra="791",
        biltil=None,
        dato=date.today,
        person="TEST",
        selgernummer=None,
        bestilling=data,
        arsak=None,
        mode=Operation.BESTILLING,
    )
