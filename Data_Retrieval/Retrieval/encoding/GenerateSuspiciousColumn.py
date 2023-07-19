import pandas as pd
import os
import shutil
import numpy as np

import New_Constant_Result as cons
#import New_Constant_Treatment as cons
# import New_Constant_Diagnosis as cons

INPUT_DIR = cons.INPUT_DIR
OUTPUT_DIR = cons.OUTPUT_DIR

class SuspiciousColumnGenerator:
    def __init__(self, input_path):
        self.input_path = input_path
        self.suspicious_data = []

    def list_files(self, dir):
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        return files
        
    def is_start_with_letter(self, data):
        data = data.strip('"')  # Remove double quotes from both ends
        if data and isinstance(data, str) and (data[0].isalpha() or data == '-1099'):
           return False
        return True


    def generate(self):
        input_files = self.list_files(self.input_path)
        for input_file in input_files:
            csv_path = os.path.join(self.input_path, input_file)
            print(csv_path)

            df_raw = pd.read_csv(csv_path, low_memory=False)
            df_raw.fillna('-1099', inplace=True)
            
#result
            target_columns = df_raw.columns[df_raw.columns.str.contains(
                    'primary_cause_of_death_ICD10'
                    '|secondary_cause_of_death_ICD10'
                 )]

#treatment
#           target_columns = df_raw.columns[df_raw.columns.str.contains(
#                    'Operative_procedures_OPCS4'
#                    '|Operative_procedures_main_OPCS4'
#                    '|Operative_procedures_secondary_OPCS4'
#                )]
                
#diagnosis
#           target_columns = df_raw.columns[df_raw.columns.str.contains(
#                    'main_cancer_diagnosis_result/first_in_patient_diagnoses_main_ICD10'
#                    '|other_cancer_diagnosis_result/diagnoses_secondary_ICD10'
#                    '|main_cancer_diagnosis_result/cancer_type_ICD10'
#                    '|other_cancer_diagnosis_result/external_causes_ICD10'
#                    '|main_cancer_diagnosis_result/first_in_patient_diagnoses_main_ICD9'
#                    '|main_cancer_diagnosis_result/cancer_type_ICD9'
#                    '|other_cancer_diagnosis_result/diagnoses_secondary_ICD9'
#                )]
            
            df_target = df_raw.loc[:, target_columns]

            self.checkSuspiciousColumns(df_target, target_columns)

        self.saveSuspiciousColumns()

    def checkSuspiciousColumns(self, df, target_columns):
        for col in target_columns:
            for index, data in df[col].items():
                if self.is_start_with_letter(str(data)):
                    self.suspicious_data.append([col, index, data])

    def saveSuspiciousColumns(self):
        suspicious_df = pd.DataFrame(self.suspicious_data, columns=['Column Name', 'Row Index', 'Suspicious Data'])
        suspicious_path = os.path.join(OUTPUT_DIR, 'SuspiciousColumn.csv')
        suspicious_df.to_csv(suspicious_path, header=True, index=False)


def create_output_dir():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)


def main():
    create_output_dir()

    suspiciousColumnGenerator = SuspiciousColumnGenerator(INPUT_DIR)
    suspiciousColumnGenerator.generate()


if __name__ == "__main__":
    main()

