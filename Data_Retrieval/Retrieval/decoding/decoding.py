#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA  02110-1301, USA.

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

















