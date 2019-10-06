import os
import datetime
import requests

from fundamental_screener.writers import make_dir_if_missing

# Our data source:
# https://uk.advfn.com/p.php?pid=filterx
# You may need to visit the URL first before it allows you to download via Python...odd.
ADVFN_URL = 'https://uk.advfn.com/p.php?pid=filterxdownload&show=1_1_,2_14_,2_26_,1_53_,1_11_,2_10_,2_5_,2_22_,3_30_,3_14_,2_56_,3_1_,3_25_,3_21_,3_3_,3_2_,1_43_,1_5_,1_8_,1_91_,1_12_,1_32_,1_3_,1_6_,1_90_,1_4_&sort=2_26_D&cnstr=&zip=0'


def get_fundamentals(download_dir, return_name=True):
    make_dir_if_missing(download_dir)
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d")
    out_filepath = os.path.join(download_dir, timestamp+'.csv')
    if not os.path.isfile(out_filepath):
        s = requests.Session()
        response = s.get(ADVFN_URL)
        with open(out_filepath, "wb") as f:
            f.write(response.content)
            f.close()
    if return_name:
        return os.path.basename(out_filepath).split('.')[0]
