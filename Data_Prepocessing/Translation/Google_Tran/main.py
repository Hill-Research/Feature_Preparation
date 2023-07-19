import glob
import os
import re
import sys

import pandas as pd
from googletrans import Translator

excel_pattern = r"(*).xlsx*"


def translate(raw_data_file):
    translator = Translator()
    data_frame = pd.read_excel(raw_data_file)

    ori_name = data_frame.columns[0]
    data_frame = data_frame.rename(columns={ori_name: 'English'})
    chinese_words = []
    numRecords = data_frame.shape[0]
    for i in range(0, numRecords):
        word = data_frame.iat[i, 0]
        translations = translator.translate(word, dest='chinese (simplified)')
        chinese_words.append(translations.text)
    data_frame['chinese'] = chinese_words
    return data_frame


def get_all_excel_files(dir):
    excel_files = glob.glob(os.path.join(dir, "*.xlsx*"))
    return excel_files


def usage():
    print("python autotranslate.py [directory of excel files]")


def gen_output_file_name(file):
    input_file_name = os.path.basename(file)
    result = re.findall('(.*).xlsx*', input_file_name)
    if (len(result) != 1):
        print("Invalid input file name ", input_file_name)
        exit(-1)
    return result[0] + "_translate.xlsx"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid command line options!")
        usage()
        exit(-1)
    dir = sys.argv[1]

    outdir = dir + "_translate"
    if os.path.isdir(outdir):
        print("Output directory ", outdir, " already exists!")
        exit(-1)
    os.makedirs(outdir)
    files = get_all_excel_files(dir)
    for file in files:
        out_frame = translate(file)
        out_file_name = gen_output_file_name(file)
        out_frame.to_excel(os.path.join(outdir) + "/" + out_file_name, index = False)
