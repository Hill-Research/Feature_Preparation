import pandas as pd
import os
import shutil
import numpy as np

INPUT_FILE = "../encoding/sample/diagnosis.csv"
def generate():
    df_raw = pd.read_csv(INPUT_FILE, low_memory=False)

    df_raw.dropna()
    df_raw.fillna('-1099', inplace=True)
    # result
    target_columns = df_raw.columns[df_raw.columns.str.contains(
        'ICD9'
    )]
    print(target_columns)


generate()

















