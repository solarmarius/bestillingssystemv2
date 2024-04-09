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

def send_email(bilfra, biltil, dato, person, selgernummer, bestilling, arsak, mode):
    print("Bestilling:", bestilling)
    
    message = MIMEMultipart()
    message["Subject"] = "Bestilling fra Tromsø {}".format(dato)
    message["From"] = st.secrets["SENDER_ADDRESS"]
    message["To"] = st.secrets["RECEIVER_ADDRESS"]
    if mode == 1: # Varebestilling
        message.attach(MIMEText("VAREBESTILLING\nBil: {} \nBestilt til dato: {}\nSjåfør navn: {}\n\nBestilling gjelder:\n{}".format(bilfra, dato, person, bestilling)))
    if mode == 2: # Vareoverføring
        message.attach(MIMEText("VAREOVERFØRING\nBil fra: {} \nBil til: {} \nOverført dato: {}\nSjåfør navn: {}\n\nOverføringen gjelder:\n{}".format(bilfra, biltil, dato, person, bestilling)))
    if mode == 3: # Personalbestilling
        message.attach(MIMEText("PERSONALBESTILLING\nSelgernummer: {} \nBestilt til dato: {}\nSjåfør navn: {}\n\nPersonalbestilling gjelder:\n{}".format(selgernummer, dato, person, bestilling)))
    if mode == 4: # Vrakordre
        message.attach(MIMEText("VRAKORDRE\nBil: {} \nVraket dato: {}\nSjåfør navn: {}\nÅrsak: {}\n\nVrakordre gjelder:\n{}".format(bilfra, dato, person, arsak, bestilling)))  

    
    server = smtplib.SMTP(st.secrets["SMTP_SERVER_ADDRESS"], st.secrets["PORT"])
    server.starttls()
    server.ehlo()
    server.login(st.secrets["SENDER_ADDRESS"], st.secrets["SENDER_PASSWORD"])
    text = message.as_string()
    
    server.sendmail(st.secrets["SENDER_ADDRESS"], st.secrets["RECEIVER_ADDRESS"], text)
    server.quit()

if not check_password():
    st.stop()
    
bestillingsliste = pd.read_csv("bestllingslistecsvv2.csv", sep=";", converters={'Artikkelnummer': str})
# Get the DataFrame column names as a list
clist = list(bestillingsliste.columns)

# Rearrange list the way you like 
clist_new = clist[-1:]+clist[:-1]   # brings the last column in the first place

# Pass the new list to the DataFrame - like a key list in a dict 
bestillingsliste = bestillingsliste[clist_new]
smais = bestillingsliste[1:29]
multipack = bestillingsliste[29:61]
dessert = bestillingsliste[61:]

st.header("Bestillingsportal for Tromsø")

bestilling, overforing, personal, vrak = st.tabs(["Varebestilling", "Vareoverføring", "Personalbestilling", "Vrak"])

with bestilling:
    st.header("Varebestilling")
    
    bil_bes = st.selectbox("Bil:", ("790", "791", "792"), key="bil_bes", placeholder="Velg bil", index=None)

    navn_bes = st.text_input("Sjåfør navn:", key="name_bes", placeholder="Ditt navn")

    dato_bes = st.date_input("Bestilt til dato:", key="dato_bes", format="DD/MM/YYYY", value=datetime.date.today()+datetime.timedelta(days=1))
    dato_bes = dato_bes.strftime("%d.%m.%Y")


    st.write("Småis")
    smais_bes = st.data_editor(smais, hide_index=True, use_container_width=True, disabled=(2,3), key="smais_bes",
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
    multipack_bes = st.data_editor(multipack, hide_index=True, use_container_width=True, disabled=(2,3), key="multipack_bes",
                                    column_config={
                                        "Antalldpakk": st.column_config.NumberColumn(
                                            "Antall D-pakk",
                                            min_value = 0,
                                            max_value = 16,
                                            step=1
                                        ),
                                        "Artikkelnummer": None
                                })

    st.write("Desserter")
    dessert_bes = st.data_editor(dessert, hide_index=True, use_container_width=True, disabled=(2,3), key="dessert_bes",
                                column_config={
                                    "Antalldpakk": st.column_config.NumberColumn(
                                        "Antall D-pakk",
                                        min_value = 0,
                                        max_value = 16,
                                        step=1
                                        ),
                                    "Artikkelnummer": None
                                })

    st.write("Du skal bestille (dobbelsjekk!)")
    bestilling_smais = smais_bes.loc[smais_bes["Antalldpakk"] != 0]
    bestilling_multipack = multipack_bes.loc[multipack_bes["Antalldpakk"] != 0]
    bestilling_dessert = dessert_bes.loc[dessert_bes["Antalldpakk"] != 0]

    bestilling_bes = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
    st.data_editor(bestilling_bes, use_container_width=True, hide_index=True, disabled=True, key="bestilling_bes")

    bestilling_email = ""

    with st.form(key="bestillingsform_bes", border=False):
        if (bil_bes == None or navn_bes == None or dato_bes == None):
            st.write("Bil / dato / navn må være fyllt ut!")
            submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary", disabled=True)
        else:
            submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary")
            
        if submitted:
            for rad in bestilling_bes.index:
                artnr = str(bestilling_bes["Artikkelnummer"][rad])
                artnavn = str(bestilling_bes["Artikkelnavn"][rad])
                antalldpakk = str(bestilling_bes["Antalldpakk"][rad])
                bes = "{} | {} | {}\n".format(artnr, artnavn, antalldpakk)
                print("Rad:", bes, "\n")
                bestilling_email += bes
            send_email(bilfra=bil_bes, 
                       biltil=None, 
                       dato=dato_bes, 
                       person=navn_bes, 
                       selgernummer=None, 
                       bestilling=bestilling_email, 
                       arsak=None, 
                       mode=1)
            st.write("Bestilling sendt inn for {}, av {}, den {}".format(bil_bes, navn_bes, dato_bes))
            st.write("Du kan nå lukke appen.")
            
with overforing:
    st.header("Vareoverføring")
    
    bilfra_ov = st.selectbox("Bil:", ("790", "791", "792"), key="bilfra_ov", placeholder="Velg bil fra", index=None)
    biltil_ov = st.selectbox("Bil:", ("790", "791", "792"), key="biltil_ov", placeholder="Velg bil til", index=None)
    
    if (bilfra_ov != None or biltil_ov != None) and (bilfra_ov == biltil_ov):
        st.write("Bil fra og Bil til er det samme!")

    navn_ov = st.text_input("Sjåfør navn:", key="name_ov", placeholder="Ditt navn")

    dato_ov = st.date_input("Overført dato:", key="dato_ov", format="DD/MM/YYYY", value=datetime.date.today()+datetime.timedelta(days=1))
    dato_ov = dato_ov.strftime("%d.%m.%Y")

    st.write("Småis")
    smais_ov = st.data_editor(smais, hide_index=True, use_container_width=True, disabled=(2,3), key="smais_ov",
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
    multipack_ov = st.data_editor(multipack, hide_index=True, use_container_width=True, disabled=(2,3), key="multipack_ov",
                                    column_config={
                                        "Antalldpakk": st.column_config.NumberColumn(
                                            "Antall D-pakk",
                                            min_value = 0,
                                            max_value = 16,
                                            step=1
                                        ),
                                        "Artikkelnummer": None
                                })

    st.write("Desserter")
    dessert_ov = st.data_editor(dessert, hide_index=True, use_container_width=True, disabled=(2,3), key="dessert_ov",
                                column_config={
                                    "Antalldpakk": st.column_config.NumberColumn(
                                        "Antall D-pakk",
                                        min_value = 0,
                                        max_value = 16,
                                        step=1
                                        ),
                                    "Artikkelnummer": None
                                })

    st.write("Du skal overføre (dobbelsjekk!)")
    bestilling_smais = smais_ov.loc[smais_ov["Antalldpakk"] != 0]
    bestilling_multipack = multipack_ov.loc[multipack_ov["Antalldpakk"] != 0]
    bestilling_dessert = dessert_ov.loc[dessert_ov["Antalldpakk"] != 0]

    bestilling_ov = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
    st.data_editor(bestilling_ov, use_container_width=True, hide_index=True, disabled=True, key="bestiling_ov")

    bestilling_email = ""

    with st.form(key="bestillingsform_ov", border=False):
        
        if (bilfra_ov == None or biltil_ov == None or navn_ov == None or dato_ov == None):
            st.write("Bil / dato / navn må være fyllt ut!")
            submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary", disabled=True)
        else:
            submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary")
            
        if submitted:
            for rad in bestilling_ov.index:
                artnr = str(bestilling_ov["Artikkelnummer"][rad])
                artnavn = str(bestilling_ov["Artikkelnavn"][rad])
                antalldpakk = str(bestilling_ov["Antalldpakk"][rad])
                bes = "{} | {} | {}\n".format(artnr, artnavn, antalldpakk)
                print("Rad:", bes, "\n")
                bestilling_email += bes
            send_email(bilfra=bilfra_ov, 
                       biltil=biltil_ov,
                       dato=dato_ov, 
                       person=navn_ov, 
                       selgernummer=None, 
                       bestilling=bestilling_email, 
                       arsak=None, 
                       mode=2)
            st.write("Overføring sendt inn fra bil {}, til bil {}, den {}".format(bilfra_ov, biltil_ov, dato_ov))
            st.write("Du kan nå lukke appen.")

with personal:
    st.header("Personalbestilling")

    navn_per = st.text_input("Sjåfør navn:", key="name_per", placeholder="Ditt navn")
    nummer_per = st.text_input("Selgernummer:", key="nummer_per", placeholder="Ditt selgernummer")

    dato_per = st.date_input("Bestillt til dato:", key="dato_per", format="DD/MM/YYYY", value=datetime.date.today()+datetime.timedelta(days=1))
    dato_per = dato_per.strftime("%d.%m.%Y")
    
    st.write("NB: Du bestiller D-pakk. Merk antall på isene, spesielt på multipacks!")

    st.write("Småis")
    smais_per = st.data_editor(smais, hide_index=True, use_container_width=True, disabled=(2,3), key="smais_per",
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
    multipack_per = st.data_editor(multipack, hide_index=True, use_container_width=True, disabled=(2,3), key="multipack_per",
                                    column_config={
                                        "Antalldpakk": st.column_config.NumberColumn(
                                            "Antall D-pakk",
                                            min_value = 0,
                                            max_value = 16,
                                            step=1
                                        ),
                                        "Artikkelnummer": None
                                })

    st.write("Desserter")
    dessert_per = st.data_editor(dessert, hide_index=True, use_container_width=True, disabled=(2,3), key="dessert_per",
                                column_config={
                                    "Antalldpakk": st.column_config.NumberColumn(
                                        "Antall D-pakk",
                                        min_value = 0,
                                        max_value = 16,
                                        step=1
                                        ),
                                    "Artikkelnummer": None
                                })

    st.write("Du skal personalbestille (dobbelsjekk!)")
    bestilling_smais = smais_per.loc[smais_per["Antalldpakk"] != 0]
    bestilling_multipack = multipack_per.loc[multipack_per["Antalldpakk"] != 0]
    bestilling_dessert = dessert_per.loc[dessert_per["Antalldpakk"] != 0]

    bestilling_per = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
    st.data_editor(bestilling_per, use_container_width=True, hide_index=True, disabled=True, key="bestiling_per")

    bestilling_email = ""

    with st.form(key="bestillingsform_per", border=False):
        
        if (navn_per == None or dato_per == None or nummer_per == None):
            st.write("Navn / selgernummer / dato må være fyllt ut!")
            submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary", disabled=True)
        else:
            submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary")
            
        if submitted:
            for rad in bestilling_per.index:
                artnr = str(bestilling_per["Artikkelnummer"][rad])
                artnavn = str(bestilling_per["Artikkelnavn"][rad])
                antalldpakk = str(bestilling_per["Antalldpakk"][rad])
                bes = "{} | {} | {}\n".format(artnr, artnavn, antalldpakk)
                print("Rad:", bes, "\n")
                bestilling_email += bes
            send_email(bilfra=None, 
                       biltil=None,
                       dato=dato_per, 
                       person=navn_per, 
                       selgernummer=nummer_per, 
                       bestilling=bestilling_email, 
                       arsak=None, 
                       mode=3)
            st.write("Personalbestilling sendt inn for {} den {}".format(navn_per, dato_per))
            st.write("Du kan nå lukke appen.")

with vrak:
    st.header("Vrakordre")
    
    bil_vrak = st.selectbox("Bil:", ("790", "791", "792"), key="bil_vrak", placeholder="Velg bil", index=None)

    navn_vrak = st.text_input("Sjåfør navn:", key="name_vrak", placeholder="Ditt navn")

    dato_vrak = st.date_input("Bestilt til dato:", key="dato_vrak", format="DD/MM/YYYY", value=datetime.date.today()+datetime.timedelta(days=1))
    dato_vrak = dato_vrak.strftime("%d.%m.%Y")


    st.write("Småis")
    smais_vrak = st.data_editor(smais, hide_index=True, use_container_width=True, disabled=(2,3), key="smais_vrak",
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
    multipack_vrak = st.data_editor(multipack, hide_index=True, use_container_width=True, disabled=(2,3), key="multipack_vrak",
                                    column_config={
                                        "Antalldpakk": st.column_config.NumberColumn(
                                            "Antall D-pakk",
                                            min_value = 0,
                                            max_value = 16,
                                            step=1
                                        ),
                                        "Artikkelnummer": None
                                })

    st.write("Desserter")
    dessert_vrak = st.data_editor(dessert, hide_index=True, use_container_width=True, disabled=(2,3), key="dessert_vrak",
                                column_config={
                                    "Antalldpakk": st.column_config.NumberColumn(
                                        "Antall D-pakk",
                                        min_value = 0,
                                        max_value = 16,
                                        step=1
                                        ),
                                    "Artikkelnummer": None
                                })

    arsak_vrak = st.text_input("Årsak:", key="arsak_vrak", placeholder="Hva er årsaken til å vrake isen?")

    st.write("Du skal vrake (dobbelsjekk!)")
    bestilling_smais = smais_vrak.loc[smais_vrak["Antalldpakk"] != 0]
    bestilling_multipack = multipack_vrak.loc[multipack_vrak["Antalldpakk"] != 0]
    bestilling_dessert = dessert_vrak.loc[dessert_vrak["Antalldpakk"] != 0]

    bestilling_vrak = pd.concat([bestilling_smais, bestilling_multipack, bestilling_dessert])
    st.data_editor(bestilling_vrak, use_container_width=True, hide_index=True, disabled=True, key="bestilling_vrak")

    bestilling_email = ""

    with st.form(key="bestillingsform_vrak", border=False):
        if (bil_vrak == None or navn_vrak == None or dato_vrak == None or arsak_vrak == None):
            st.write("Bil / dato / navn / årsak må være fyllt ut!")
            submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary", disabled=True)
        else:
            submitted = st.form_submit_button("Send inn", use_container_width=True, type="primary")
            
        if submitted:
            for rad in bestilling_vrak.index:
                artnr = str(bestilling_vrak["Artikkelnummer"][rad])
                artnavn = str(bestilling_vrak["Artikkelnavn"][rad])
                antalldpakk = str(bestilling_vrak["Antalldpakk"][rad])
                bes = "{} | {} | {}\n".format(artnr, artnavn, antalldpakk)
                print("Rad:", bes, "\n")
                bestilling_email += bes
            send_email(bilfra=bil_vrak, 
                       biltil=None, 
                       dato=dato_vrak, 
                       person=navn_vrak, 
                       selgernummer=None, 
                       bestilling=bestilling_email, 
                       arsak=arsak_vrak, 
                       mode=4)
            st.write("Vrakordre sendt inn for {}, av {}, den {}".format(bil_vrak, navn_vrak, dato_vrak))
            st.write("Du kan nå lukke appen.")