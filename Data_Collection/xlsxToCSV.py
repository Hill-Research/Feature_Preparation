import glob
import os

import pandas as pd

# Specify input/output directory
EXCEL_DIR = 'prostatic_cancer'
CSV_DIR = 'prostatic_cancer_csv'
# Create output directory if not exist
if not os.path.exists(CSV_DIR):
    os.makedirs(CSV_DIR)
# Start to do conversion
file_lists = glob.glob(EXCEL_DIR + "/*.xlsx")
for file in file_lists:
    excel_file = pd.read_excel(file)
    # Note that we remove the translation column when generating the CSV file.
    # The exact key name may subject to changes!!!!!!
    excel_file = excel_file.drop('trans', axis=1)
    excel_file_base_name = os.path.basename(file)
    csv_file_name = CSV_DIR + "/" + excel_file_base_name[:-5] + ".csv"
    excel_file.to_csv(csv_file_name, index=None, header=None)
