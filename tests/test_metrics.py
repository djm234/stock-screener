import pandas as pd
from hamcrest import (
    assert_that, equal_to
)

from fundamental_screener import metrics


def test_return_max():
    df = pd.DataFrame().from_dict(
        {
            'ROI': [
                10,
                10,
            ],
            'ROCE': [
                10,
                20,
            ],
        }
    )
    result = metrics.return_max(df)
    assert_that(
        result['return_max'].tolist(),
        equal_to(
            [10, 20]
        )
    )


def test_magic_formula():
    df = pd.DataFrame().from_dict(
        {
            'Stock name': [
                'A',
                'B',
                'C',
                'D',
            ],
            'Earnings Yield': [
                5,
                10,
                1,
                6,
            ],
            'ROI': [
                25,
                12,
                3,
                9,
            ],
        }
    )
    result = metrics.magic_formula(df)
    assert_that(
        result['Stock name'].tolist(),
        equal_to(
            ['B', 'A', 'D', 'C']
        )
    )
    assert_that(
        result['MF rank'].tolist(),
        equal_to(
            [1, 2, 3, 4]
        )
    )


def test_z_score():
    df = pd.DataFrame().from_dict(
        {
            'Net Working Capital To Total Assets (%)': [
                10,
                20,
            ],
            'Profit - retained (m)': [
                100,
                200,
            ],
            'Total assets (m)': [
                200,
                400,
            ],
            'Total equity (m)': [
                1,
                1000,
            ],
            'Total liabilities (m)': [
                2,
                4,
            ],
            'Turnover (m)': [
                20,
                40000,
            ],
            'Profit - pre tax (m)': [
                50,
                100,
            ]
        }
    )
    result = metrics.z_score(df)
    assert_that(
        result['Z score'].tolist(),
        equal_to(
            [2.045, 251.765]
        )
    )


def test_f_score():
    df = pd.DataFrame().from_dict(
        {
            'Net Income Of Revenues(%)': [
                1,
            ],
            'Return On Assets (%)': [
                1,
            ],
            'Operations (m)': [
                10,
            ],
            'Total assets (m)': [
                100,
            ],
            'Current ratio': [
                2,
            ],
            'Quick ratio (Acid Test)': [
                2
            ],
        }
    )
    result = metrics.f_score(df)
    assert_that(
        result['F score(ish)'].tolist(),
        equal_to(
            [5]
        )
    )


def test_pence_to_pounds():
    df = pd.DataFrame().from_dict(
        {
            'Price currency': [
                'GBX',
                'GBP',
            ],
            "Yesterday's close": [
                10,
                10,
            ],
        }
    )
    result = metrics.pence_to_pounds(df)
    assert_that(
        result['price_in_pounds'].tolist(),
        equal_to(
            [0.1, 10]
        )
    )


def test_long_term_momentum():
    df = pd.DataFrame().from_dict(
        {
            'RS 90': [
                90,
            ],
            'RS 180': [
                180,
            ],
            'RS 1y': [
                365,
            ],
            'RS 3y': [
                365*3,
            ],
            'RS 5y': [
                365*5,
            ],
        }
    )
    result = metrics.long_term_momentum(df)
    assert_that(
        result.iloc[0]['linreg_long'],
        equal_to(
            {
                'slope': 1.0,
                'intercept': 0.0,
                'r_value': 1.0,
                'p_value': 1.5000000000000099e-40,
                'std_err': 0.0
            }
        )
    )


def test_short_term_momentum():
    df = pd.DataFrame().from_dict(
        {
            'RS 90': [
                90,
            ],
            'RS 180': [
                180,
            ],
            'RS 1y': [
                365,
            ],
            'RS 3y': [
                365*3,
            ],
            'RS 5y': [
                365*5,
            ],
        }
    )
    result = metrics.short_term_momentum(df)
    assert_that(
        result.iloc[0]['linreg_short'],
        equal_to(
            {
                'slope': 1.0,
                'intercept': 0.0,
                'r_value': 1.0,
                'p_value': 9.999999999999998e-21,
                'std_err': 0.0
            }
        )
    )


def test_percentile_list():
    assert_that(
        list(metrics.percentile_list(3)),
        equal_to(
            [100, 50, 0]
        )
    )
