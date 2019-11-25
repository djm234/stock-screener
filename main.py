import os
import streamlit as st
import pandas as pd
from functools import partial

from fundamental_screener import (
    download, parsers, writers, screen_styles
)

DOWNLOAD_DIR = '_downloads'
RESULT_DIR = '_results'
REPROCESS_ALL = False
INTERACTIVE = True

st.title("Fundamental stock screener")
st.sidebar.header("Settings")
st.sidebar.subheader("Dataset choice")

if st.sidebar.button("Download today's data"):
    download.get_fundamentals(DOWNLOAD_DIR)
    all_fundamentals_snapshots = parsers.find_files_in_dir(DOWNLOAD_DIR)

all_fundamentals_snapshots = parsers.find_files_in_dir(DOWNLOAD_DIR)
filepath = st.sidebar.selectbox(
    'Select date',
    options=all_fundamentals_snapshots
)


screen_types = {
    'None': None,
    'dividend_screen': screen_styles.dividend_screener,
    'value_screen': screen_styles.value_screener,
    'magic_formula_screen': screen_styles.magic_formula_screener,
    'momentum_screen': screen_styles.momentum_screener,
    'quality_screen': screen_styles.quality_screener,
    'cash_rich_screen': screen_styles.cash_rich_screener,
    #'QVM': partial(screen_styles.custom_screen, screens=['quality', 'value', 'momentum']),
    'custom': None,
}
screen_choice = st.sidebar.radio(
    "Choose screen type",
    options=list(screen_types.keys())
)

if screen_choice == 'custom':
    custom_choices = st.multiselect(
        'Select screens to combine',
        options=[
            'cash_rich',
            'quality',
            'value',
            'momentum',
            'dividend',
            'magic_formula',
        ]
    )
    custom_screen = partial(screen_styles.custom_screen, screens=custom_choices)

# Open snapshot file
df = parsers.open_downloaded_data(filepath)

# Set up dataframe to include apt. properties
df = parsers.set_up_dataframe(df)

if screen_choice == 'None':
    st.dataframe(df)
elif screen_choice == 'custom':
    st.dataframe(custom_screen(df))
else:
    st.dataframe(screen_types[screen_choice](df))
