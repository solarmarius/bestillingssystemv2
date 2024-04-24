"""
Imports the rawfiles (csv), and setup dataframes
Also functions to change the data in csv (to be used by admin)
"""

import streamlit as st
import pandas as pd


def change_cols(data: pd.DataFrame) -> pd.DataFrame:
    """
    Pulls antalldpakk and antallfpakk to front
    """
    # Get column names as list
    clist = list(data.columns)

    # Rearrange list
    clist_new = clist[-1:] + clist[:-1]
    clist_new = clist_new[-1:] + clist_new[:-1]

    # Pass new list to dataframes
    new_data = data[clist_new]
    return new_data


def change_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Given a change in the dataframe (from admin),
    update the csv file to reflect this
    """
    pass


smais_data = pd.read_csv("data/smais.csv", sep=";", converters={"Artikkelnummer": str})
multipack_data = pd.read_csv(
    "data/multipacks.csv", sep=";", converters={"Artikkelnummer": str}
)
desserter_data = pd.read_csv(
    "data/dessert.csv", sep=";", converters={"Artikkelnummer": str}
)


def create_smais(keyname: str, mode=0):
    """
    Returns a data editor for småis
    """
    if mode == 0:
        smais = st.data_editor(
            smais_data,
            hide_index=True,
            use_container_width=True,
            disabled=(2, 3, 4),
            key=keyname,
            column_config={
                "Antalldpakk": st.column_config.NumberColumn(
                    "Antall D-pakk", min_value=0, max_value=16, step=1
                )
            },
            column_order=("Antalldpakk", "Artikkelnavn"),
        )
    # To display F-pakk (vrak og telling)
    if mode == 1:
        smais = st.data_editor(
            smais_data,
            hide_index=True,
            use_container_width=True,
            disabled=(1, 2),
            key=keyname,
            column_config={
                "Antalldpakk": st.column_config.NumberColumn(
                    "Antall D-pakk", min_value=0, step=1
                ),
                "Antallfpakk": st.column_config.NumberColumn(
                    "Antall F-pakk", min_value=0, step=1
                ),
            },
            column_order=("Antalldpakk", "Antallfpakk", "Artikkelnavn"),
        )

    return smais


def create_multipack(keyname: str, mode=0):
    """
    Returns a data editor for multipack
    """
    if mode == 0:
        multipack = st.data_editor(
            multipack_data,
            hide_index=True,
            use_container_width=True,
            disabled=(2, 3, 4),
            key=keyname,
            column_config={
                "Antalldpakk": st.column_config.NumberColumn(
                    "Antall D-pakk", min_value=0, max_value=16, step=1
                )
            },
            column_order=("Antalldpakk", "Artikkelnavn"),
        )
    if mode == 1:
        multipack = st.data_editor(
            multipack_data,
            hide_index=True,
            use_container_width=True,
            disabled=(1, 2),
            key=keyname,
            column_config={
                "Antalldpakk": st.column_config.NumberColumn(
                    "Antall D-pakk", min_value=0, step=1
                ),
                "Antallfpakk": st.column_config.NumberColumn(
                    "Antall F-pakk", min_value=0, step=1
                ),
            },
            column_order=("Antalldpakk", "Antallfpakk", "Artikkelnavn"),
        )
    return multipack


def create_dessert(keyname: str, mode=0):
    """
    Returns a data editor for desserter
    """
    if mode == 0:
        desserter = st.data_editor(
            desserter_data,
            hide_index=True,
            use_container_width=True,
            disabled=(2, 3, 4),
            key=keyname,
            column_config={
                "Antalldpakk": st.column_config.NumberColumn(
                    "Antall D-pakk", min_value=0, max_value=16, step=1
                )
            },
            column_order=("Antalldpakk", "Artikkelnavn"),
        )
    if mode == 1:
        desserter = st.data_editor(
            desserter_data,
            hide_index=True,
            use_container_width=True,
            disabled=(1, 2),
            key=keyname,
            column_config={
                "Antalldpakk": st.column_config.NumberColumn(
                    "Antall D-pakk", min_value=0, step=1
                ),
                "Antallfpakk": st.column_config.NumberColumn(
                    "Antall F-pakk", min_value=0, step=1
                ),
            },
            column_order=("Antalldpakk", "Antallfpakk", "Artikkelnavn"),
        )
    return desserter


def combine_data(data_1: pd.DataFrame, data_2: pd.DataFrame) -> pd.DataFrame:
    """
    Adds two dataframes based on its artikkelnummer
    """
    data_1 = data_1.reset_index()
    data_2 = data_2.reset_index()
    for index, row in data_1.iterrows():
        key = row["Artikkelnummer"]
        data_2rad = data_2.loc[data_2["Artikkelnummer"] == key]

        new_dpakk = int(row["Antalldpakk"]) + int(data_2rad.iloc[0]["Antalldpakk"])

        data_1.at[index, "Antalldpakk"] = new_dpakk

        new_fpakk = int(row["Antallfpakk"]) + int(data_2rad.iloc[0]["Antallfpakk"])

        data_1.at[index, "Antallfpakk"] = new_fpakk

    return data_1


def combine_pakk(data: pd.DataFrame) -> pd.DataFrame:
    """
    Using mapping from csv file, converts the f-pakk to d-pakk and returns combined dataframe
    """
    data = data.astype({"Antalldpakk": "float64"})
    data = data.reset_index(drop=True)
    map_data = pd.read_csv("data/ismap.csv", sep=";")
    for index, row in data.iterrows():
        key = int(row["Artikkelnummer"])

        # Hvor mange fpakk
        fpakk = float(row["Antallfpakk"])

        # Hente rett divisor som matcher artikkelnummer
        divisor = map_data.loc[map_data["Artikkelnummer"] == key]
        divisor = float(divisor.iloc[0]["Forhold"])

        # Antall fpakk som brøk av dpakk
        value = fpakk / divisor

        # Hvor mange dpakk
        dpakk = float(row["Antalldpakk"])

        # Replace verdi i dataen
        data.at[index, "Antalldpakk"] = dpakk + value

    return data


if __name__ == "__main__":
    data = create_dessert("test", mode=1)

    data_2 = create_dessert("test2", mode=1)

    comb = combine_data(data, data_2)
    print(comb)

    pakkcomb = combine_pakk(comb)
    print(pakkcomb)
