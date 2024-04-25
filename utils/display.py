import streamlit as st


def menu():
    """
    Shows the menu
    """
    ### MAIN INTERFACE ###
    st.header("Bestillingsportal for Region Nord")

    # Menu
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.page_link("pages/bestilling.py", label="Varebestilling", icon="📬")

    with col2:
        st.page_link("pages/overforing.py", label="Vareoverføring", icon="↪️")

    with col3:
        st.page_link("pages/personal.py", label="Personalbestilling", icon="💁")

    with col4:
        st.page_link("pages/vrak.py", label="Vrak", icon="🗑️")

    with col5:
        st.page_link("pages/telling.py", label="Telling", icon="📋")

    st.divider()
