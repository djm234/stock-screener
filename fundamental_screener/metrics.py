def return_max(df):
    # Calculate the highest return
    df['return_max'] = df[['ROCE', 'ROI']].apply(lambda row: max(row), axis=1)
    return df


def magic_formula(df):
    # Greenblatts Magic Formula
    # Sort by earnings yield and calculate rank
    df = df.sort_values(by='Earnings Yield', ascending = False)
    df['earnings_rank_percentile'] = [(i/len(df))*100 for i in range(1,len(df)+1)]
    # Same for ROI (ROIC)
    df = df.sort_values(by='ROI', ascending = False)
    df['ROI_rank_percentile'] = [(i/len(df))*100 for i in range(1,len(df)+1)]
    # Sum ranks of percentiles - those at top are highest ranks
    df['magic formula score'] = df['earnings_rank_percentile'] + df['ROI_rank_percentile']
    df = df.sort_values(by='magic formula score', ascending=True)
    df['MF rank'] = [i for i in range(1,len(df)+1)]
    # Clean up
    df = df.drop(['earnings_rank_percentile', 'ROI_rank_percentile'], axis=1)
    return df


def z_score(df):
    # Altman Z score
    # a credit-strength test that gauges a publicly traded manufacturing company's likelihood of bankruptcy.
    # Z-Score = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E
    # Where:
    # A = working capital / total assets
    A = df['Net Working Capital To Total Assets (%)'] / 100.
    # B = retained earnings / total assets
    B = df['Profit - retained (m)'] / df['Total assets (m)']
    # C = earnings before interest and tax / total assets
    C = df['Profit - pre tax (m)'] / df['Total assets (m)']
    # D = market value of equity / total liabilities
    D = df['Total equity (m)'] / df['Total liabilities (m)']
    # E = sales / total assets
    E = df['Turnover (m)'] / df['Total assets (m)']
    # Sum up
    df['Z score'] = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E
    return df


def f_score(df):
    # Piotrovsky's F-Score (partial - missing data required to calculate!)
    """
    A. Profitability Signals
        1. Net Income [DONE] – Score 1 if there is positive net income in the current year.
        2. Operating Cash Flow [DONE] - Score 1 if there is positive cashflow from operations in the current year.
        3. Return on Assets [DONE] – Score 1 if the ROA is higher in the current period compared to the previous year.
        4. Quality of Earnings [DONE] – Score 1 if the cash flow from operations exceeds net income before extraordinary items.
    B. Leverage, Liquidity and Source of Funds
        5. Decrease in leverage – Score 1 if there is a lower ratio of long term debt to in the current period compared value in the previous year .
        6. Increase in liquidity – Score 1 if there is a higher current ratio this year compared to the previous year.
            - N/A - instead, see if current ratio and quick ratio is good
        7. Absence of Dilution – Score 1 if the Firm did not issue new shares/equity in the preceding year.
    C. Operating Efficiency
        8. Score 1 if there is a higher gross margin compared to the previous year.
        9. Asset Turnover – Score 1 if there is a higher asset turnover ratio year on year (as a measure of productivity).
    """
    def _f(row):
        score = 0
        if row['Net Income Of Revenues(%)']>0:
            score += 1
        if row['Return On Assets (%)']>0:
            score += 1
        if row['Operations (m)']>0:
            score += 1
        if row['Total assets (m)'] < 0:
            if (row['Operations (m)']/row['Total assets (m)']) > row['Return On Assets (%)']:
                score += 1
        # Estimate Point 6
        if row['Current ratio'] >= 1.5:
            score += 0.5
        if  row['Quick ratio (Acid Test)'] > 1:
            score += 0.5
        return score
    # There are currently a max of 5 points to be awarded.
    # If this was a full F score, usually anything greater than 5
    # 5/9 = 55%. 55% of 5 is 2.77. Therefore, round down and suggest 2.5 score is good to filter for
    df['F score(ish)'] = df.apply(lambda row: _f(row), axis=1)
    return df


def pence_to_pounds(df):
    def _convert_to_gbp(row):
        if row['Price currency'] == 'GBX':
            return row["Yesterday's close"]/100
        elif row['Price currency'] == 'GBP':
            return row["Yesterday's close"]
        else:
            raise AssertionError
    df['price_in_pounds'] = df.apply(lambda row: _convert_to_gbp(row), axis=1)
    return df
