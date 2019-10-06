from fundamental_screener import filters


def dividend_screener(df):
    df2 = df.copy()
    # A good return on capital
    df2 = df2[df2['ROI'].apply(lambda x: x>=12)]
    # A Price-to Earnings ratio that is not too large
    df2 = df2[df2['PE ratio']<=15]
    # A Price-to-Earnings Growth ratio not oo high
    df2 = df2[df2['PEG factor'].apply(lambda x: 0.<x<=2)]
    # A high Z-score indicates protection from bankruptcy
    df2 = df2[df2['Z score']>=3]
    # If the company pays a dividend this must not be too high
    df2 = filters.filter_unfavourable_dividend_yield(df2)
    # If the company pays a dividend this must have a decent cover
    df2 = filters.filter_unfavourable_dividend_cover(df2)
    # Avoid short term reversion to mean by making sure price is below a limit
    df2 = filters.avoid_short_term_negative_reversion_to_mean(df2)
    # Store result with most informative rows first
    display_cols = ['Name', 'Industry name', 'MF rank', 'Market cap. (m)', 'price_in_pounds', 'PE ratio', 'PEG factor', 'Dividend yield', 'Dividend cover', 'Z score', 'F score (p)', 'ROI']
    df2 = df2[display_cols + [c for c in df2.columns if c not in display_cols]]
    return df2
