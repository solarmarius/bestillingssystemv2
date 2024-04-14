# Todo

13.04: Redirect eventuelle errors til en email som sendes til meg

13.04: FOR FLERE DEPOTER: Endre bil_input til å display relevante biler for depotet
    - Endre også "Bestillinsportal for {DEPOT}"!

13.04: Endre nummer inputs (nå er det text_input) slik at bare tall kan insertes!!

13.04: Changes til en dataframe blir oppdatert til session state, etter submit button, clear the session state
    - Pga at en kan bestille varer, også etterpå vrake. Hva skjer da?

13.04: Implementere streamlit-authenticator, legge til login form i start-interface, hvis login er riktig (admin), redirect til admin.py page

OK 13.04: Visuelt endre til å være mer overends med brand
OK 13.04: Kompartemize de ulike tabene til main interface
OK 13.04: Legg til kollone med F-pakk i csv og data, og bruke hide arg i data_editor
OK 13.04: Endre raw dataframe slik at den display rekkefølgen i csv; endre rekkefølge i selve dataeditor med column_order
OK 13.04: Simplifisere - trenger vi en ny data_editor for hver tab? Kan vi ha en felles for alle? (Unntatt vrak)
OK 13.04: Endre data_editor/dataframes at man ikke bruker slicing (hva om vi må legge til iser, slette iser)? 

# Ideer

- Implementere login for "admin", kan endre dataframe (legge til, fjerne iser), og kode for hvert depot og mulighet for å legge inn nye depot
    - Bruke streamlit-authentication, eller streamlit-keyclock og sette opp Keycloak server.
    - En "admin" bruker som kan legge til nye brukere, slette osv. 

EKSEMPEL USERFLOW FOR MARKEDSANSVARLIG
- Display ulike dataframes (småis, multipacks og desserte), kan klikke på en rad for å endre den eller slette den. Kan legge til nye rad (nye iser), må da fylle ut artikkelunummer og artikkelnavn. Denne blir sortert alfabetisk automatisk, og csv filen som main program bruker blir oppdatert. 

- Implementere ulike koder (logins) for hvert depot, dette endrer SECRETS slik at man kan konfigurere hvilken epost (lager) man sender til 
- Koble backend til (FastAPI), finne ut hvordan man kan deploye til en server (Heroku?)