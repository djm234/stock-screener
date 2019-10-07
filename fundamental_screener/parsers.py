import pandas as pd
import glob
import os

from fundamental_screener import filters, metrics

DISPLAY_COLS = [
    'Name', 'Industry name', 'MF rank', 'Market cap. (m)', 'price_in_pounds',
    'PE ratio', 'PEG factor', 'Dividend yield', 'Dividend cover', 'Z score',
    'F score(ish)', 'ROI'
]


def find_files_in_dir(dirpath, extension='.csv'):
    return glob.glob(os.path.join(dirpath, f'*{extension}'))


def open_downloaded_data(filepath):
    df = pd.read_csv(filepath, encoding='ISO-8859-1', index_col=False)
    df = df.set_index('Symbol')
    df = df.drop('Unnamed: 0', axis=1)
    return df


def set_up_dataframe(df):
    # Formatting some cols
    df = df.rename(
        columns={
            'ROI - Return On Investments (%)': 'ROI',
            'Pc Change from 180 days Open Price': 'RS 180',
            'Pc Change from Qtr Open Price': 'RS 90',
            'Return On Capital Employed (ROCE)': 'ROCE',
        }
    )
    # Keep companies trading in the currency we are interested in.
    df = filters.filter_non_british_currency(df)

    # Convert anything in pence to pounds
    df = metrics.pence_to_pounds(df)
    # Calculate Greenblatt's Magic Formula ranking
    df = metrics.magic_formula(df)
    # Calculate Piotrovsky's F-Score
    df = metrics.f_score(df)
    # Calculate Altman Z-Score
    df = metrics.z_score(df)
    # Add max return col (ROI and ROCE max)
    df = metrics.return_max(df)

    # Abbreviate contents
    df['Industry name'] = df['Industry name'].apply(lambda x: str(x).split(' ')[0])
    return df[DISPLAY_COLS + [c for c in df.columns if c not in DISPLAY_COLS]]
