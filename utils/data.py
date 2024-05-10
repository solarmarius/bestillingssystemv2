"""
Imports the rawfiles (csv), and setup dataframes
Also functions to change the data in csv (to be used by admin)
"""

import streamlit as st
import pandas as pd

from utils.enums import Mode
from utils import logger

SMAIS_FILE = "data/smais.csv"
MULTIPACK_FILE = "data/multipacks.csv"
DESSERT_FILE = "data/dessert.csv"

try:
    smais_data = pd.read_csv(SMAIS_FILE, sep=";", converters={"Artikkelnummer": str})
except FileNotFoundError:
    logger.error(f"File {SMAIS_FILE} not found.")
    smais_data = pd.DataFrame()

try:
    multipack_data = pd.read_csv(
        MULTIPACK_FILE, sep=";", converters={"Artikkelnummer": str}
    )
except FileNotFoundError:
    logger.error(f"File {MULTIPACK_FILE} not found.")
    multipack_data = pd.DataFrame()

try:
    desserter_data = pd.read_csv(
        DESSERT_FILE, sep=";", converters={"Artikkelnummer": str}
    )
except FileNotFoundError:
    logger.error(f"File {DESSERT_FILE} not found.")
    desserter_data = pd.DataFrame()

COLUMN_CONFIGS = {
    Mode.DEFAULT: {
        "Antalldpakk": st.column_config.NumberColumn(
            "Antall D-pakk", min_value=0, max_value=18, step=1
        )
    },
    Mode.DISPLAY_FPAKK: {
        "Antalldpakk": st.column_config.NumberColumn(
            "Antall D-pakk", min_value=0, step=1
        ),
        "Antallfpakk": st.column_config.NumberColumn(
            "Antall F-pakk", min_value=0, step=1
        ),
    },
}

DISABLED_COLUMNS = {
    Mode.DEFAULT: (2,),
    Mode.DISPLAY_FPAKK: (1, 2),
}

COLUMNS_ORDER = {
    Mode.DEFAULT: ("Antalldpakk", "Artikkelnavn"),
    Mode.DISPLAY_FPAKK: ("Antalldpakk", "Antallfpakk", "Artikkelnavn"),
}


def create_smais(keyname: str, mode: Mode) -> pd.DataFrame:
    """
    Returns a data editor for småis.

    Parameters:
    - keyname (str): The keyname for the data editor.
    - mode (Mode): The mode for the data editor.

    Returns:
    - pd.DataFrame: The data editor for småis.
    """
    return st.data_editor(
        smais_data,
        hide_index=True,
        use_container_width=True,
        disabled=DISABLED_COLUMNS[mode],
        key=keyname,
        column_config=COLUMN_CONFIGS[mode],
        column_order=COLUMNS_ORDER[mode],
    )


def create_multipack(keyname: str, mode: Mode) -> pd.DataFrame:
    """
    Returns a data editor for multipack.

    Parameters:
    - keyname (str): The keyname for the data editor.
    - mode (Mode): The mode for the data editor.

    Returns:
    - pd.DataFrame: The data editor for multipack.
    """
    return st.data_editor(
        multipack_data,
        hide_index=True,
        use_container_width=True,
        disabled=DISABLED_COLUMNS[mode],
        key=keyname,
        column_config=COLUMN_CONFIGS[mode],
        column_order=COLUMNS_ORDER[mode],
    )


def create_dessert(keyname: str, mode=0) -> pd.DataFrame:
    """
    Returns a data editor for desserter.

    Parameters:
    - keyname (str): The keyname for the data editor.
    - mode (int, optional): The mode for the data editor. Defaults to 0.

    Returns:
    - pd.DataFrame: The data editor for desserter.

    """
    return st.data_editor(
        desserter_data,
        hide_index=True,
        use_container_width=True,
        disabled=DISABLED_COLUMNS[mode],
        key=keyname,
        column_config=COLUMN_CONFIGS[mode],
        column_order=COLUMNS_ORDER[mode],
    )


def combine_data(data_1: pd.DataFrame, data_2: pd.DataFrame) -> pd.DataFrame:
    """
    Adds two dataframes based on its artikkelnummer

    Parameters:
    - data_1 (pd.DataFrame): The first dataframe to be combined
    - data_2 (pd.DataFrame): The second dataframe to be combined

    Returns:
    - pd.DataFrame: The combined dataframe

    """
    data_1 = data_1.reset_index()
    data_2 = data_2.reset_index()
    for index, row in data_1.iterrows():
        key = row["Artikkelnummer"]
        name = row["Artikkelnavn"]
        data_2rad = data_2.loc[data_2["Artikkelnummer"] == key]

        try:
            new_dpakk = int(row["Antalldpakk"]) + int(data_2rad.iloc[0]["Antalldpakk"])
        except Exception as e:
            st.error(
                f"Verdi under {name} er satt til 'None' i tabellen. Vennligst endre den til 0."
            )

        data_1.at[index, "Antalldpakk"] = new_dpakk

        try:
            new_fpakk = int(row["Antallfpakk"]) + int(data_2rad.iloc[0]["Antallfpakk"])
        except Exception as e:
            st.error(
                f"Verdi under {name} er satt til 'None' i tabellen. Vennligst endre den til 0."
            )

        data_1.at[index, "Antallfpakk"] = new_fpakk

    return data_1


def combine_pakk(data: pd.DataFrame) -> pd.DataFrame:
    """
    Using mapping from csv file, converts the f-pakk to d-pakk and returns combined dataframe

    Parameters:
    - data (pd.DataFrame): The input dataframe containing the data to be processed.

    Returns:
    - pd.DataFrame: The combined dataframe with f-pakk converted to d-pakk.
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
