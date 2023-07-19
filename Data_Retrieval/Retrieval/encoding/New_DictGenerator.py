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

#要改5
# import New_Constant_Result as cons
import New_Constant_Treatment as cons
# import New_Constant_Diagnosis as cons
# import New_Constant_Basic as cons

INPUT_DIR = cons.INPUT_DIR
OUTPUT_DIR = cons.OUTPUT_DIR


class DictGenerator:
    def __init__(self, input_path):
        self.input_path = input_path
        self.unique_set = set()

    def list_files(self, dir):
        """
        Get the list of files in the directory
        @param dir: file directory
        @return: a list of files in the directory
        """
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        return files

    
    def generate(self):
        input_files = self.list_files(self.input_path)
        for input_file in input_files:
            csv_path = os.path.join(self.input_path, input_file)
            print(csv_path)
            # print(len(cons.COLUMN_NAME))
            # print(len(set(cons.COLUMN_NAME)))
            # df_raw = pd.read_csv(csv_path, names=cons.COLUMN_NAME)
            df_raw = pd.read_csv(csv_path)

            # 要改6
            # # result
            # df_target = df_raw.loc[:, lambda d: d.columns.str.contains('ICD10')]  # 只提取需要处理的column

            # treatment
            target_lst = df_raw.columns.str.contains('OPCS') & ~df_raw.columns.str.contains('time')
            df_target = df_raw.loc[:, target_lst]

            # # diagnosis
            # target_lst = df_raw.columns.str.contains('main_cancer_diagnosis_result/first_in_patient_diagnoses_main_ICD10') \
            #             | df_raw.columns.str.contains('other_cancer_diagnosis_result/diagnoses_secondary_ICD10') \
            #             | df_raw.columns.str.contains('main_cancer_diagnosis_result/cancer_type_ ICD10') \
            #             | df_raw.columns.str.contains('other_cancer_diagnosis_result/external_causes_ICD10') \
            #             | df_raw.columns.str.contains('main_cancer_diagnosis_result/first_in_patient_diagnoses_main_ICD9') \
            #             | df_raw.columns.str.contains('main_cancer_diagnosis_result/cancer_type_ ICD9') \
            #             | df_raw.columns.str.contains('other_cancer_diagnosis_result/diagnoses_secondary_ICD9')
            # df_target = df_raw.loc[:, target_lst]

            # # basic
            # target_lst = df_raw.columns.str.contains('allergy_history_result/allergy') | df_raw.columns.str.contains('/eye_problems') \
            #             | df_raw.columns.str.contains('/teeth_dental_problems') \
            #             | df_raw.columns.str.contains('/hearing_problems') \
            #             | df_raw.columns.str.contains('/heart_attack') \
            #             | df_raw.columns.str.contains('/angina') | df_raw.columns.str.contains('/stroke') \
            #             | df_raw.columns.str.contains('/high_blood_pressure') | df_raw.columns.str.contains('/deep_vein_thrombosis') \
            #             | df_raw.columns.str.contains('/pulmonary_embolism') | df_raw.columns.str.contains('/emphysema_bronchitis') \
            #             | df_raw.columns.str.contains('/asthma') | df_raw.columns.str.contains('/diabetes') \
            #             | df_raw.columns.str.contains('/cancer') | df_raw.columns.str.contains('/other_serious_medical_condition')      
            # df_target = df_raw.loc[:, target_lst]

            df = df_target.fillna("-1009")  # Fill All NA as -1009
            csv_set = self.getUniqueSet(df)
            print(list(csv_set))
            self.unique_set = self.unique_set.union(csv_set)
        return self.genEncodeDict()


    def getUniqueSet(self, df):
        unique_set = set()
        for col in df.columns:
            unique_set = unique_set.union(set(df[col].unique().tolist()))
        return unique_set


    def genEncodeDict(self):
        # print(self.unique_set)
        self.unique_set.remove('-1009')
        unique_list = list(self.unique_set)

        unique_dict = dict()
        for i in range(1, len(unique_list) + 1):
            unique_dict[unique_list[i - 1]] = i
        unique_dict['-1009'] = -1009

        encodeDict_df = pd.DataFrame.from_dict(unique_dict, orient='index')
        encodeDict_df_output_path = os.path.join(OUTPUT_DIR, 'encodeDict.csv')
        encodeDict_df.to_csv(encodeDict_df_output_path)

        return unique_dict

def create_output_dir():
    """
    Create output directory. If old directory exists, then delete it
    @return: None
    """
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)


def main():
    create_output_dir()

    # 用来生成字典的一段
    dictGenerator = DictGenerator(INPUT_DIR)
    encodeDict = dictGenerator.generate()
    
    # 动态生成字典
    # encodeDict_df = pd.DataFrame.from_dict(encodeDict, orient='index')
    # encodeDict_df_output_path = os.path.join(OUTPUT_DIR, 'encodeDict')
    # encodeDict_df.to_csv(encodeDict_df_output_path)


if __name__ == "__main__":
    main()