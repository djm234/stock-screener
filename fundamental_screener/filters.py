import pandas as pd

CURRENCIES = {
    'GBX': 'pence sterling',
    'GBP': 'pounds sterling'
}


def filter_non_british_currency(df):
    return df[df['Price currency'].isin(CURRENCIES.keys())]


def filter_unfavourable_dividend_yield(df):
    def _filter_div(x):
        if pd.isnull(x):
            return True
        elif 0 < x <= 15:
            return True
        else:
            return False
    return df[df['Dividend yield'].apply(lambda x: _filter_div(x))]


def filter_unfavourable_dividend_cover(df):
    def _filter_cover(x):
        if pd.isnull(x):
            return True
        elif x >= 1.5:
            return True
        else:
            return False
    return df[df['Dividend cover'].apply(lambda x: _filter_cover(x))]
