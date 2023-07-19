import pandas as pd
import os
import shutil
import numpy as np

RAW_DIR = 'raw'
DEID_DIR = 'result'
KEYWORD_FILE = 'keywords.txt'


def create_output_dir():
    """
    Create output directory. If old directory exists, then delete it
    @return: None
    """
    if os.path.exists(DEID_DIR):
        shutil.rmtree(DEID_DIR)
    os.makedirs(DEID_DIR)

def is_sensitive(data_field, keywords):
    for keyword in keywords:
        if keyword in data_field:
            return 1
    return 0

def list_files(dir):
    """
    Get the list of files in the directory
    @param dir: file directory
    @return: a list of files in the directory
    """
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return files


def get_keyword():
    with open(KEYWORD_FILE, "r") as key_file:
        keywords = key_file.read().splitlines()
    return keywords

def process_file(path, keywords):
    df = pd.read_csv(path, encoding ="utf-8", on_bad_lines='skip')
    for col in df:
        if is_sensitive(col, keywords):
            df[col] = ''
    file_name = os.path.basename(path)
    output_path = DEID_DIR + '/' + file_name
    df.to_csv(output_path, index=None)

def main():
    create_output_dir()
    keywords = get_keyword()
    print(keywords)
    files = list_files(RAW_DIR)
    for file in files:
        path = os.path.join(RAW_DIR, file)
        print("process raw file ", path)
        process_file(path, keywords)



if __name__ == "__main__":
    main()

