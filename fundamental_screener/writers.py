import os


def make_dir_if_missing(dirpath):
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)


def store_screen_result(df, out_dir, file_name):
    make_dir_if_missing(out_dir)
    df.to_csv(os.path.join(out_dir, f'{file_name}.csv'), index=False)
