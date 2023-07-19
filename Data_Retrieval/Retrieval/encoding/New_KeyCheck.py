import pandas as pd
import os

# import New_Constant_Result as cons
# import New_Constant_Treatment as cons
import New_Constant_Diagnosis as cons
# import New_Constant_Basic as cons

INPUT_DIR = cons.INPUT_DIR
OUTPUT_DIR = cons.OUTPUT_DIR

def main():
    # dict_df = pd.read_csv('output-result/encodeDict.csv')
    dict_df = pd.read_csv('output-treatment/encodeDict.csv')
    # dict_df = pd.read_csv('output-diagnosis/encodeDict.csv')
    # dict_df = pd.read_csv('output-basic/encodeDict.csv')
    dict_df.drop([len(dict_df)-1],inplace = True)
    dict_df.columns = ['key','value']
    dict_df['bool'] = dict_df['key'].apply(lambda row: not str.isalpha(eval(row)[0]))
    df_suspicious = dict_df.loc[dict_df['bool'],:]
    output_path = os.path.join(OUTPUT_DIR, 'suspiciousKey.csv')
    df_suspicious.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
