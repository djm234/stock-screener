import pandas as pd

CURRENCIES = {
    'GBX': 'pence sterling',
    'GBP': 'pounds sterling'
}


def filter_unwanted_industries(df):
    # Remove utilities and finance
    finance_and_utilities = ['ALTERNATIVE ENERGY', 'OIL & GAS PRODUCERS',
    'EQUITY INVESTMENT INSTRUMENTS', 'REAL ESTATE INVESTMENT & SERVICES',
    'GENERAL FINANCIAL', 'ELECTRICITY', 'REAL ESTATE INVESTMENT TRUSTS',
    'GAS WATER & UTILITIES', 'NONLIFE INSURANCE',
    'NONEQUITY INVESTMENT INSTRUMENTS', 'LIFE INSURANCE',
    'FIXED LINE TELECOMMUNICATIONS', 'BANKS', 'OIL EQUIPMENT SERVICES & DISTRIBUTION']
    df = df[~df['Industry name'].isin(finance_and_utilities)]
    return df


def filter_non_british_currency(df):
    return df[df['Price currency'].isin(CURRENCIES.keys())]


def filter_unfavourable_dividend_yield(df):
    def _filter_div(x):
        if pd.isnull(x):
            return True
        elif x <= 15:
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


def avoid_short_term_negative_reversion_to_mean(df):
    return df[
        (df['Pc Change from 180 days Open Price'].apply(lambda x: 0<x<=15)) |
        (df['Pc Change from Qtr Open Price'].apply(lambda x: 0<x<=15))
    ]
