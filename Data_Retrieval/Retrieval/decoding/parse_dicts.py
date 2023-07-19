import os
import pandas as pd
import json
import re

LIB_DIR = '/Users/yingli/Desktop/biotech/tech/ai_engineering/Data-retrieval/ukb/decoder/ukb_encoding_lib'
OUTPUT_DIR = '/Users/yingli/Desktop/biotech/tech/ai_engineering/Data-retrieval/ukb/decoder/parsed_dicts'

def parse_common(file_name, dict_name):
    file_path = os.path.join(LIB_DIR, file_name)
    df = pd.read_csv(file_path, sep='\t')
    df.set_index('coding', inplace=True)
    dict_content = df['meaning'].to_dict()
    dicts[dict_name] = dict_content

def parse_remove_first_string(file_name, dict_name):
    file_path = os.path.join(LIB_DIR, file_name)
    df = pd.read_csv(file_path, sep='\t')
    df.set_index('coding', inplace=True)
    df['meaning'] = df['meaning'].str.split(' ').str[1:].str.join(' ')
    dict_content = df['meaning'].to_dict()
    dicts[dict_name] = dict_content

# 特殊处理 OPCS3 operation codes.tsv
def parse_opcs3(file_name, dict_name):
    file_path = os.path.join(LIB_DIR, file_name)
    df = pd.read_csv(file_path, sep='\t')
    df.set_index('coding', inplace=True)
    df['meaning'] = df['meaning'].apply(lambda x: ' '.join(x.split(' ')[1:]) if re.match("^\d+.*", x) else x)
    dict_content = df['meaning'].to_dict()
    dicts[dict_name] = dict_content

FILE_LIST = ['Flag indicating Yes:True:Presence.tsv',
             'Antibiotics.tsv',
             'Calendar Month.tsv',
             'Depression substances.tsv',
             'Depression therapies.tsv',
             'Ethnic Grouping.tsv',
             'Genotyping array.tsv',
             'HES coding for DELMETH.tsv',
             'HES coding for DELPREAN and DELPOSAN.tsv',
             'Kinship level.tsv',
             'Operation.tsv',
             'Sex.tsv',
             'TAF answer-set 502.tsv',
             'TAF answer-set 503.tsv',
             'Treatments.tsv',
             'Tumour Histology.tsv',
             'Tumour behaviour.tsv',
             'Yes No dichotomous choice.tsv',
             'Yes No or Unsure.tsv',
             'Yes or No.tsv',
             'g22.i.answer.a.FH9.ans.tsv',
             'g22.i.answer.a.H5C.ans.tsv',
             'g22.i.answer.a.H6.ans:main.tsv',
             'g22.i.answer.a.H7C.ans.tsv',
             'g22.i.answer.a.L1.ans.tsv',
             'g22.i.answer.a.L2.ans.tsv',
             'g22.i.answer.a.L7.ans:main.tsv',
             'g22.i.answer.a.L7.ans:pilot.tsv',
             'g22.i.answer.a.L7A.ans:main.tsv',
             'g22.i.answer.a.L7A.ans:pilot.tsv',
             'g22.i.answer.a.L8.ans.tsv',
             'g22.i.answer.a.OP1M.ans.tsv',
             'g22.i.answer.a.S2A.ans:main.tsv',
             'g22.i.answer.a.S4AA.ans.tsv',
             'g22.i.answer.a.SY4I.ans.tsv',
             'opt_sur_any.tsv',
             'opt_sur_side.tsv'
            ]
dicts = {}

# 使用常规方式处理文件列表
for file_name in FILE_LIST:
    dict_name = os.path.splitext(file_name)[0]
    parse_common(file_name, dict_name)

# 处理特殊的三个文件
special_files = ['ICD9.tsv', 'ICD10.tsv', 'OPCS4 operation codes.tsv']
for file_name in special_files:
    dict_name = os.path.splitext(file_name)[0]
    parse_remove_first_string(file_name, dict_name)

# 处理 OPCS3 operation codes.tsv 文件
parse_opcs3('OPCS3 operation codes.tsv', 'OPCS3 operation codes')

# 保存结果到JSON文件
with open(os.path.join(OUTPUT_DIR, 'decode_dicts.json'), 'w') as f:
    json.dump(dicts, f)
