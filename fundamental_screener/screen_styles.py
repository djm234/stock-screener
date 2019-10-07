from fundamental_screener import filters


def magic_formula_screener(df):
    df2 = df.copy()
    # Sort so that most interesting companies are at the top
    df2 = df2.sort_values(by='MF rank', ascending=True)
    # Pick top 25
    return df2.head(25)


def dividend_screener(df):
    df2 = df.copy()
    # A good return on capital
    df2 = df2[df2['ROI'].apply(lambda x: x>=12)]
    # A Price-to Earnings ratio that is not too large
    df2 = df2[df2['PE ratio']<=15]
    # A Price-to-Earnings Growth ratio not oo high
    df2 = df2[df2['PEG factor'].apply(lambda x: 0.<x<=2)]
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
    df2 = df2[df2['PE ratio']<=10]
    # A Price-to-Earnings Growth ratio not oo high
    df2 = df2[df2['PEG factor'].apply(lambda x: 0.<x<=1)]
    # Good value PTB
    df2 = df2[df2['Price To Tangible Book Value']<=10]
    # Sort so that most interesting companies are at the top
    df2 = df2.sort_values(by='PE ratio', ascending=True)
    return df2


def momentum_screener(df):
    df2 = df.copy()
    # Price is greater than 180 days ago
    df2 = df2[df2['RS 180'] > 0]
    # Price is greater than 90 days ago
    df2 = df2[df2['RS 90'] > 0]
    # Price difference is greater than 180 days ago compared to now
    df2 = df2[df2['RS 180'] > df2['RS 90']]
    # Sort so that most interesting companies are at the top
    df2 = df2.sort_values(by='RS 180', ascending=False)
    return df2


def quality_screener(df):
    df2 = df.copy()
    # A high Z-score indicates protection from bankruptcy
    df2 = df2[df2['Z score']>=3]
    return df2.sort_values(by='Z score', ascending=False)


def QVM_screener(df):
    df2 = df.copy()
    # Combines multiple styles
    QVM = quality_screener(df2)
    QVM = momentum_screener(QVM)
    QVM = value_screener(QVM)
    QVM = QVM.sort_values(by='MF rank', ascending=True)
    return QVM


def stability_screener(df):

    # should be some calculation - e.g. curr price, minus 180 pc = start price. work out 90 day price pc
    # then make sure 90 pc is close to that pc

    df2 = df.copy()

    then = (df2['RS 180']/100).apply(lambda x: x*df2['price_in_pounds'] if x <=1 else x/df2['price_in_pounds'])

    #then = df2['price_in_pounds'] * (1-df2['RS 180']/100)
    now = df2['price_in_pounds']
    mid = (then+now)/2
    mid_pc = mid/now

    # The 90 day RSI is approx half way between 180 and present prices
    df2 = df2[mid_pc.apply(lambda x: 0.95 <= 1.05)]

    # The price has increased
    df2 = df2[df2['RS 180'] > 0]
    df2 = df2[df2['RS 90'] > 0]
    # Avoid short term reversion to mean by making sure price is below a limit
    df2 = df2[df2['RS 90'] <= 15]
    # And that it hasn't dropped too far recently
    #df2 = df2[df2['RS 90'] >= -5]
    # 180 day diff is greater than 1
    #df2 = df2[(df2['RS 90'] / df2['RS 180']) > 1]
    return df2.sort_values(by='RS 180', ascending=False)


SCREEN_CHOICES = {
    'dividend': dividend_screener,
    'value': value_screener,
    'magic_formula': magic_formula_screener,
    'momentum': momentum_screener,
    'quality': quality_screener,
    'stability': stability_screener,
}


def custom_screen(df, screens=[]):
    if (len(screens) == 0) or (len(set(screens).intersection(SCREEN_CHOICES.keys())) < len(screens)):
        print(f"Must enter selection of screens to use in sequence: {SCREEN_CHOICES.keys()}")
    df2 = df.copy()
    for screen in screens:
        df2 = SCREEN_CHOICES[screen](df2)
    return df2.sort_values(by='MF rank')