import os
import pandas as pd
from IPython import embed

from fundamental_screener import (
    download, parsers, metrics, writers, filters, screen_styles
)

DOWNLOAD_DIR = 'downloads'
RESULT_DIR = 'results'
REPROCESS_ALL = True
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

            # Set up dataframe to include apt. properties
            df = parsers.set_up_dataframe(df)

            # Perform screens and store the results to disk

            # Magic Formula
            magic_formula_screen = screen_styles.magic_formula_screener(df)
            writers.store_screen_result(magic_formula_screen, RESULT_DIR, f"{name}_magic_formula_screen")

            # Best dividends
            dividend_screen = screen_styles.dividend_screener(df)
            writers.store_screen_result(dividend_screen, RESULT_DIR, f"{name}_dividend_screen")

            # Best value
            value_screen = screen_styles.value_screener(df)
            writers.store_screen_result(value_screen, RESULT_DIR, f"{name}_value_screen")

            # Momentum
            momentum_screen = screen_styles.momentum_screener(df)
            writers.store_screen_result(momentum_screen, RESULT_DIR, f"{name}_momentum_screen")

            # Quality
            quality_screen = screen_styles.quality_screener(df)
            writers.store_screen_result(quality_screen, RESULT_DIR, f"{name}_quality_screen")

            # Stable increase in price
            stability_screen = screen_styles.stability_screener(df)
            writers.store_screen_result(stability_screen, RESULT_DIR, f"{name}_stability_screen")

            # Custom Quality, Value, and Momentum screen
            QVM = screen_styles.custom_screen(df, screens=['quality', 'value', 'momentum'])
            writers.store_screen_result(QVM, RESULT_DIR, f"{name}_QVM")

            # If we have processed the latest data, keep note of this
            if name == latest:
                # Store latest data subsets
                latest_screens = {
                    'dividend_screen': dividend_screen,
                    'value_screen': value_screen,
                    'magic_formula_screen': magic_formula_screen,
                    'momentum_screen': momentum_screen,
                    'quality_screen': quality_screen,
                    'QVM': QVM,
                    'stability_screen': stability_screen,
                }
                # Store whole table
                result = df.copy()

    print(f"Latest result - {latest}:")
    for k, v in latest_screens.items():
        top = 10
        print(f'\n{k.upper()} {len(v)} stocks (top {top}):')
        PRINT_COLS = [
            'Name', 'MF rank', 'Industry name', 'Market cap. (m)', 'price_in_pounds',
            'F score(ish)', 'Z score', 'PE ratio', 'PEG factor',
            'Dividend yield', 'Dividend cover',
            'RS 180', 'RS 90'
        ]
        print(v[PRINT_COLS].head(top))

    if INTERACTIVE:
        print("\nLatest data in an object called 'result'\n")
        embed()
