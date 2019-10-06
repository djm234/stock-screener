import os
import pandas as pd
from IPython import embed

from fundamental_screener import (
    download, parsers, metrics, writers, filters, screen_styles
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

            # Set up dataframe to include apt. properties
            df = parsers.set_up_dataframe(df)

            # Perform a screen
            dividend_screen = screen_styles.dividend_screener(df)
            # Store the result to disk
            writers.store_screen_result(dividend_screen, RESULT_DIR, f"{name}_dividend_screen")

            # If we have processed the latest data, keep note of this
            if name == latest:
                latest_screens = {
                    'dividend_screen': dividend_screen,
                }
                result = df.copy()

    print(f"Latest result - {latest}:")
    for k, v in latest_screens.items():
        print(k)
        print(v)

    if INTERACTIVE:
        print("\nLatest data in an object called 'result'\n")
        embed()
