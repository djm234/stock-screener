import pandas as pd
import glob
import os

from fundamental_screener import filters, metrics


def find_files_in_dir(dirpath, extension='.csv'):
    return glob.glob(os.path.join(dirpath, f'*{extension}'))


def open_downloaded_data(filepath):
    df = pd.read_csv(filepath, encoding='ISO-8859-1', index_col=False)
    df = df.set_index('Symbol')
    df = df.drop('Unnamed: 0', axis=1)
    return df


def set_up_dataframe(df):
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

    # Formatting some cols
    df = df.rename(columns={'ROI - Return On Investments (%)': 'ROI'})
    # Abbreviate contents
    df['Industry name'] = df['Industry name'].apply(lambda x: str(x).split(' ')[0])
    return df
