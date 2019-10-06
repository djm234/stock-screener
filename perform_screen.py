import os
import pandas as pd
from IPython import embed

from fundamental_screener import (
    download, parsers, metrics, writers, filters
)

DOWNLOAD_DIR = 'downloads'
RESULT_DIR = 'results'
REPROCESS_ALL = False
INTERACTIVE = True

if __name__ == '__main__':
    # Get the most recent set of fundamentals from ADVFN
    latest = download.get_fundamentals(DOWNLOAD_DIR)

    # Get a list of all the snapshots that have been downloaded previously
    all_fundamentals_snapshots = parsers.find_files_in_dir(DOWNLOAD_DIR)

    # Iterate over each snapshot
    for filepath in all_fundamentals_snapshots:
        name = os.path.basename(filepath).split('.')[0]
        if (name == latest) or REPROCESS_ALL:
            print(f"Processing {name}")

            # Open snapshot file
            df = parsers.open_downloaded_data(filepath)
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

            # A good return on capital
            df = df[df['ROI'].apply(lambda x: x>=12)]
            # A Price-to Earnings ratio that is not too large
            df = df[df['PE ratio']<=10]
            # A Price-to-Earnings Growth ratio not oo high
            df = df[df['PEG factor'].apply(lambda x: 0.<x<=1.6)]
            # A high Z-score indicates protection from bankruptcy
            df = df[df['Z score']>=3]
            # If the company pays a dividend this must not be too high
            df = filters.filter_unfavourable_dividend_yield(df)
            # If the company pays a dividend this must have a decent cover
            df = filters.filter_unfavourable_dividend_cover(df)
            # Avoid short term reversion to mean by making sure price is below a limit
            df = filters.avoid_short_term_negative_reversion_to_mean(df)

            # Store result with most informative rows first
            display_cols = ['Name', 'Industry name', 'MF rank', 'Market cap. (m)', 'price_in_pounds', 'PE ratio', 'PEG factor', 'Dividend yield', 'Dividend cover', 'Z score', 'F score (p)', 'ROI']
            writers.store_screen_result(df[display_cols + [c for c in df.columns if c not in display_cols]], RESULT_DIR, name)

            # If we have processed the latest data, keep note of this
            if name == latest:
                result = df.copy()

    print(f"Latest result - {latest}:\n{result[display_cols]}")
    if INTERACTIVE:
        print("\nLatest data in an object called 'result'\n")
        embed()
