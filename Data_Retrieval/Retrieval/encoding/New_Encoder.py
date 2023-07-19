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

#要改3
# import New_Constant_Result as cons
import New_Constant_Treatment as cons
# import New_Constant_Diagnosis as cons
# import New_Constant_Basic as cons

class Encoder:
    def __init__(self, path, encodeDict):
        """
        Initialize the Encoder.
        @param path: specifies the CSV file which needs to be encoded
        """
        self.encodeDict = encodeDict
        # df_raw = pd.read_csv(path, names=cons.COLUMN_NAME)
        df_raw = pd.read_csv(path)
        self.df_raw = df_raw

        #要改4
        # result
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

        self.target_columns = df_target.columns.to_list()
        self.df = df_target.fillna("-1009")  # Fill All NA as -1

    def encode(self):
        """
        Encode the dataframe data fields based on the dictionary.
        @todo we are assuming that each column in the dataframe should be encoded, which is not always true
        @return: encoded dataframe
        """
        encodingDict = self.encodeDict
        for col in self.df.columns:
            self.df[col] = self.df[col].map(lambda cell: encodingDict[cell])

    def dump(self, output_path):
        """
        Dump the encoded dataframe into output file
        @param output_path: the file handler to the output file
        @return: None
        """
        ## 用df_target 替换df_raw里对应的列
        self.df_raw.loc[ : , self.target_columns] = self.df
        self.df_raw.to_csv(output_path, index=False)
