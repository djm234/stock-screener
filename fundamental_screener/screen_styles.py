from fundamental_screener import filters


def magic_formula_screener(df):
    df2 = df.copy()
    # Sort so that most interesting companies are at the top
    df2 = df2.sort_values(by='MF rank', ascending=True)
    # Filter according to additional fields on stockopedia
    df2 = df2[(df2['Market cap. (m)'] >= 30) & (df2['earnings_rank_percentile'] < 99) & (df2['ROI_rank_percentile'] < 99)]
    # Pick top 25
    return df2.head(50)


def dividend_screener(df):
    df2 = df.copy()
    # If the company pays a dividend this must not be too high
    df2 = filters.filter_unfavourable_dividend_yield(df2)
    # If the company pays a dividend this must have a decent cover
    df2 = filters.filter_unfavourable_dividend_cover(df2)
    # Sort so that most interesting companies are at the top
    df2 = df2.sort_values(by='Dividend yield', ascending=False)
    return df2


def value_screener(df):
    df2 = df.copy()
    # A Price-to Earnings ratio that is not too large
    df2 = df2[df2['PE ratio'] <= 15]
    # A Price-to-Earnings Growth ratio not oo high
    df2 = df2[df2['PEG factor'].apply(lambda x: 0. < x <= 2)]
    # Good value PTB
    df2 = df2[df2['Price To Tangible Book Value'] <= 10]
    # Sort so that most interesting companies are at the top
    df2 = df2.sort_values(by='PE ratio', ascending=True)
    return df2


def momentum_screener(df):
    df2 = df.copy()
    df2 = df2[(df2['lt_momentum_score'] >= 80) | (df2['st_momentum_score'] >= 80)]
    # Sort so that most interesting companies are at the top
    df2 = df2.sort_values(by='st_momentum_score', ascending=False)
    return df2


def quality_screener(df):
    df2 = df.copy()
    # A high Z-score indicates protection from bankruptcy
    df2 = df2[df2['Z score'] >= 3]
    df2 = df2[df2['F score(ish)'] >= 2.5] # 2.5 because we don't have enough data to fully calculate
    return df2.sort_values(by='Z score', ascending=False)


def cash_rich_screener(df):
    df2 = df.copy()
    # Return max is highest out of ROI and ROCE
    df2 = df2[df2['return_max']>=10]
    # Lots of cash compared to earnings per share
    df2 = df2[(df2['Cash flow PS']/df2['Earnings PS - basic']) >= 0.8]
    return df2.sort_values(by='return_max', ascending=False)


SCREEN_CHOICES = {
    'dividend': dividend_screener,
    'value': value_screener,
    'magic_formula': magic_formula_screener,
    'momentum': momentum_screener,
    'quality': quality_screener,
    'cash_rich': cash_rich_screener,
}


def custom_screen(df, screens=[]):
    if (len(screens) == 0) or (len(set(screens).intersection(SCREEN_CHOICES.keys())) < len(screens)):
        print(f"Must enter selection of screens to use in sequence: {SCREEN_CHOICES.keys()}")
    df2 = df.copy()
    for screen_name in screens:
        df2 = SCREEN_CHOICES[screen_name](df2)
    return df2.sort_values(by='MF rank')
