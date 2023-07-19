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

import pandas as pd

LIB_DIR = 'ukb_encoding_lib'

dict = {}
pattern = r'[0-9]'


def list_files(dir):
    """
    Get the list of files in the directory
    @param dir: file directory
    @return: a list of files in the directory
    """
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return files


def remove_coding(str):
    words = str.split()
    # print(" ".join(words[1:]))
    return " ".join(words[1:])


def get_coding(str):
    return str.split()[0]


def parse(file):
    df = pd.read_csv(file, sep='\t')
    meanings = df.get('meaning')
    codings = meanings.apply(get_coding)
    norm_meanings = meanings.apply(remove_coding)
    dict = pd.Series(norm_meanings.to_list(), index=codings).to_dict()
    print(dict)


def main():
    lib_files = list_files(LIB_DIR)
    for lib_file in lib_files:
        lib_path = os.path.join(LIB_DIR, lib_file)
        print("process lib file ", lib_path)
        if 'ICD9' in lib_file:
            parse(lib_path)


if __name__ == "__main__":
    main()
