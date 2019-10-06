import pandas as pd
import glob
import os


def find_files_in_dir(dirpath, extension='.csv'):
    return glob.glob(os.path.join(dirpath, f'*{extension}'))


def open_downloaded_data(filepath):
    df = pd.read_csv(filepath, encoding='ISO-8859-1', index_col=False)
    df = df.set_index('Symbol')
    df = df.drop('Unnamed: 0', axis=1)
    return df
