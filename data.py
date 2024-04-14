"""
Imports the rawfiles (csv), and setup dataframes
Also functions to change the data in csv (to be used by admin)
"""

import streamlit as st
import pandas as pd

def change_cols(data:pd.DataFrame)->pd.DataFrame:
    """
    Pulls antalldpakk and antallfpakk to front
    """
    # Get column names as list
    clist = list(data.columns)
    
    # Rearrange list 
    clist_new = clist[-1:]+clist[:-1]
    clist_new = clist_new[-1:]+clist_new[:-1]
    
    # Pass new list to dataframes
    new_data = data[clist_new]
    return new_data

def change_data(data: pd.DataFrame)->pd.DataFrame:
    """
    Given a change in the dataframe (from admin),
    update the csv file to reflect this
    """
    pass

smais_data = pd.read_csv("data/smais.csv", sep=";", converters={'Artikkelnummer': str})
multipack_data = pd.read_csv("data/multipacks.csv", sep=";", converters={'Artikkelnummer': str})
desserter_data = pd.read_csv("data/dessert.csv", sep=";", converters={'Artikkelnummer': str})

def create_smais():
    """
    Returns a data editor for småis
    """

    smais = st.data_editor(smais_data, hide_index=True, use_container_width=True, disabled=(2,3,4), key="smais",
                                column_config={
                                    "Antalldpakk": st.column_config.NumberColumn(
                                        "Antall D-pakk",
                                        min_value = 0,
                                        max_value = 16,
                                        step=1
                                    )}, 
                                column_order=("Antalldpakk", "Artikkelnavn"))

    return smais

def create_multipack():
    """
    Returns a data editor for multipack
    """
    multipack = st.data_editor(multipack_data, hide_index=True, use_container_width=True, disabled=(2,3,4), key="multipack",
                                column_config={
                                    "Antalldpakk": st.column_config.NumberColumn(
                                        "Antall D-pakk",
                                        min_value = 0,
                                        max_value = 16,
                                        step=1
                                    )}, 
                                column_order=("Antalldpakk", "Artikkelnavn"))

    return multipack


def create_dessert():
    """
    Returns a data editor for desserter
    """
    desserter = st.data_editor(desserter_data, hide_index=True, use_container_width=True, disabled=(2,3,4), key="desserter",
                                column_config={
                                    "Antalldpakk": st.column_config.NumberColumn(
                                        "Antall D-pakk",
                                        min_value = 0,
                                        max_value = 16,
                                        step=1
                                    )}, 
                                column_order=("Antalldpakk", "Artikkelnavn"))

    return desserter

if __name__ == "__main__":
    pass