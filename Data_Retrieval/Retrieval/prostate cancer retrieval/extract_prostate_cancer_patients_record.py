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

file_name = 'ukb670004.tab'
col_ids = {}  # Initialize as an empty dictionary
col_names = {}  # Initialize as an empty dictionary

def gen_cols(base, first_range, second_range, name):
    for i in range(0, first_range):
        for j in range(0, second_range):
            new_col_id = 'f.' + str(base) + '.' + str(i) + '.' + str(j)
            new_col_name = name + "_" + str(i) + '.' + str(j)

            key = int(base) * 100 + int(i) * 10 + int(j) * 1
            col_ids[key] = new_col_id
            col_names[key] = new_col_name


def prepare_searching_indexes():
    gen_cols(34, 1, 1, 'Birth_Year')
    gen_cols(52, 1, 1, 'Birth_Month')
    gen_cols(31, 1, 1, 'Sex')
#lab_indicator
    gen_cols(3809,4,1,'time_since_last_PSA')
    gen_cols(2365,4,1,'Ever_had_PSA')
    gen_cols(12224,4,1,'Abdominal_MRI_complete')
    gen_cols(12223,4,1,'Abdominal_MRI_method')
    gen_cols(12140,4,1,'Believe_safe_to_abdominal_MRI')
#treatment
    gen_cols(41272,1,124,'OPCS4')
    gen_cols(41273,1,16,'OPCS3')
    gen_cols(41200,1,55,'OPCS4_main')
    gen_cols(41210,1,97,'OPCS4_second')
    gen_cols(41256,1,13,'OPCS3_main')
    gen_cols(41258,1,5,'OPCS3_second')
    gen_cols(2415,4,1,'had_major_operation')
    gen_cols(2844,4,1,'had_other_major_operation')
    gen_cols(20011,4,32,'age_of_operation')
    gen_cols(20010,4,32,'year_of_operation')
    gen_cols(20014,4,32,'method_of_record_time')
    gen_cols(136,4,1,'num_of_operations')
    gen_cols(137,4,1,'num_of_medication_taken')
    gen_cols(20003,4,48,'medicine_code')
    gen_cols(6671,4,1,'num_of_antibiotics_last3month')
    gen_cols(20199,4,4,'antibiotic_codes_last3month')
    gen_cols(20551,1,4,'medication_addiction')
    gen_cols(6153,4,4,'exogenous_hormones')
    gen_cols(2814,4,1,'Ever_used_HRT')
    gen_cols(3536,4,1,'Age_started_HRT')
    gen_cols(3546,4,1,'Age_last_used_HRT')
    

#results
    gen_cols(20001,4,6,'Cancer_Code') 
    gen_cols(40018,2,1,'death_record_format')
    gen_cols(40020,2,1,'death_record_origin')
    gen_cols(40000,2,1,'date_of_death')
    gen_cols(40007,2,1,'Age_at_death')
    gen_cols(40001,2,1,'primary_cause_of_death_ICD10')
    gen_cols(40002,2,15,'secondary_cause_of_death_ICD10')
    gen_cols(40010,1,1,'Description_cause_of_death')
    gen_cols(40012,22,1,'Behavior_of_cancer_tumour')
    gen_cols(41270,1,242,'Diagnoses_ICD10')
    gen_cols(41280,1,242,'date_first_in_patient_diagnosis_ICD10')
    gen_cols(41271,1,47,'Diagnoses_ICD9')
    gen_cols(41281,1,47,'date_first_in_patient_diagnosis_ICD9')
    gen_cols(41202,1,79,'Diagnoses_main_ICD10')
    gen_cols(41262,1,79,'date_first_in_patient_diagnosis_main_ICD10')
    gen_cols(41203,1,28,'Diagnoses_main_ICD9')
    gen_cols(41263,1,28,'date_first_in_patient_diagnosis_main_ICD9')
    gen_cols(41204,1,188,'diagnoses_secondary_ICD10')
    gen_cols(41205,1,30,'diagnoses_secondary_ICD9')
    gen_cols(41201,1,22,'external_causes_ICD10')
    gen_cols(84,4,6,'Cancer_first_occurred_age_year')
    gen_cols(20007,4,6,'Interpolated_age')
    gen_cols(20009,4,34,'Interpolated_age_non_cancer_first_diagnosed')
    gen_cols(20006,4,6,'Interpolated_year_cancer_first_diagnosed')
    gen_cols(20008,4,34,'Interpolated_year_non_cancer_first_diagnosed')
    gen_cols(20012,4,6,'Method_of_recording_time_cancer_first_diagnosed')
    gen_cols(20013,4,34,'Method_of_recording_time_non_cancer_first_diagnosed')
    gen_cols(20002,4,34,'Non_cancer_illness_code')
    gen_cols(87,4,34,'Non_Cancer_first_occurred_age_year')
    gen_cols(134,4,1,'num_self_reported_cancers')
    gen_cols(135,4,1,'num_self_reported_non_cancer')
#followup
    gen_cols(21027,1,1,'Abdominal_discomfort_6month_longer')
    gen_cols(21057,1,1,'pain_intercourse_last_3month')
    gen_cols(21061,1,1,'sleeping_troublr_last_3month')
    gen_cols(21058,1,1,'urinary_frequency_bladder_irritability_last3month')
    gen_cols(21041,1,1,'abdominal_pain_in_general')
    gen_cols(54,4,1,'assessment_centre_MET_Scores')
    gen_cols(22035,1,1,'above_moderate_vigorous_recommendation')
    gen_cols(22036,1,1,'Above_moderate_vigorous_walking_recommendation')
    gen_cols(22032,1,1,'IPAQ_activity_group')
    gen_cols(22038,1,1,'MET_minutes_week_moderate_activity')
    gen_cols(22039,1,1,'MET_minutes_week_vigorous_activity')
    gen_cols(22037,1,1,'MET_minutes_week_walking')
    gen_cols(22033,1,1,'Summed_days_activity')
    gen_cols(22034,1,1,'Summed_minutes_activity')




def main():
    prepare_searching_indexes()
    print(col_ids)
    print(col_names)
#
    number_of_records = 50000

    actual_columns = pd.read_csv(file_name, sep='\t', nrows=0).columns
    # Sort the keys
    sorted_keys = sorted(col_ids.keys())

    # Extract the sorted column IDs and column names
    sorted_col_ids = [col_ids[key] for key in sorted_keys]
    sorted_col_names = [col_names[key] for key in sorted_keys]

    actual_col_ids = [col_id for col_id in sorted_col_ids if col_id in actual_columns]
    actual_col_names = [col_name for col_id, col_name in zip(sorted_col_ids, sorted_col_names) if col_id in actual_columns]

    df = pd.read_csv(file_name, sep = '\t', skiprows = 500001, nrows=number_of_records, on_bad_lines = 'skip', names = actual_columns,  usecols = actual_col_ids)
    df.columns = actual_col_names

    # Generate the cancer_code_columns list
    cancer_code_columns = [f'Cancer_Code_{i}.{j}' for i in range(4) for j in range(6)]

    df_filtered = df[df[cancer_code_columns].apply(lambda x: any(x == 1044), axis=1)]

    print(df_filtered)

    df_filtered.to_csv('output_prostatic_cancer_test11.csv', index=False)
# DtypeWarning: Columns?
if __name__ == "__main__":
    main()

