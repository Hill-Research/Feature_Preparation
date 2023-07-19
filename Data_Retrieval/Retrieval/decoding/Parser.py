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
