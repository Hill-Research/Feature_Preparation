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

import os
import shutil

import pandas as pd

from New_Encoder import Encoder
from Concat import Concat
from New_DictGenerator import DictGenerator

## 要改1
# import New_Constant_Result as cons
import New_Constant_Treatment as cons
# import New_Constant_Diagnosis as cons
# import New_Constant_Basic as cons

INPUT_DIR = cons.INPUT_DIR
OUTPUT_DIR = cons.OUTPUT_DIR


def list_files(dir):
    """
    Get the list of files in the directory
    @param dir: file directory
    @return: a list of files in the directory
    """
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return files


def create_output_dir():
    """
    Create output directory. If old directory exists, then delete it
    @return: None
    """
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)



def main():
    print('MAIN START')
    # 要改2
    # dict_df = pd.read_csv('output-result/encodeDict.csv')
    dict_df = pd.read_csv('output-treatment/encodeDict.csv')
    # dict_df = pd.read_csv('output-diagnosis/encodeDict.csv')
    # dict_df = pd.read_csv('output-basic/encodeDict.csv')
    encodeDict = dict()

    def add_csv_to_dict(row):
        # print(row[0], row[1]
        encodeDict[row[0]] = row[1]

    dict_df.apply(add_csv_to_dict, axis=1)

    input_files = list_files(INPUT_DIR)
    for input_file in input_files:
        # TODO: should iterate over all files
        # if "result" not in input_file: continue
        input_path = os.path.join(INPUT_DIR, input_file)
        print("process file ", input_path)
        encoder = Encoder(input_path, encodeDict)
        encoder.encode()
        output_path = os.path.join(OUTPUT_DIR, input_file)
        print("output file: ", output_path)
        encoder.dump(output_path)
    print('MAIN END')


if __name__ == "__main__":
    main()
