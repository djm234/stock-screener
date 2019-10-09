import pandas as pd
from hamcrest import (
    assert_that, contains_inanyorder
)

from fundamental_screener import filters


def test_filter_non_british_currency():
    df = pd.DataFrame().from_dict(
        {
            'Price currency': [
                'GBX',
                'GBP',
                'other',
            ],
        }
    )
    result = filters.filter_non_british_currency(df)
    assert_that(
        result['Price currency'].tolist(),
        contains_inanyorder(
            'GBP', 'GBX'
        )
    )


def test_filter_unfavourable_dividend_yield():
    df = pd.DataFrame().from_dict(
        {
            'Dividend yield': [
                0,
                5,
                25,
            ],
        }
    )
    result = filters.filter_unfavourable_dividend_yield(df)
    assert_that(
        result['Dividend yield'].tolist(),
        contains_inanyorder(
            5
        )
    )


def test_filter_unfavourable_dividend_cover():
    df = pd.DataFrame().from_dict(
        {
            'Dividend cover': [
                0,
                1,
                2,

            ]
        }
    )
    result = filters.filter_unfavourable_dividend_cover(df)
    assert_that(
        result['Dividend cover'].tolist(),
        contains_inanyorder(
            2
        )
    )
