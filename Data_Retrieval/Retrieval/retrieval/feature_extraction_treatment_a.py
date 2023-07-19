

                                                       
import pandas as pd
import re
import sys
import numpy as np
import os
import shutil

def gen_cols(item):
    base, first_range, second_range, name = int(item[0]),int(item[1]),int(item[2]),str(item[3])
    col_ids = []
    col_names = []
    for i in range(0, first_range):
        for j in range(0, second_range):
            new_col_id = 'f.' + str(base) + '.' + str(i) + '.' + str(j)
            new_col_name = name + "_" + str(i) + '.' + str(j)
            col_ids.append(new_col_id)
            col_names.append(new_col_name)
    return col_ids, col_names
OUTPUT_DIR='treatment_out'
file_path = r'CSV-UKB-Features-Design_treatment.csv'
df = pd.read_csv(file_path)

nan_positions = df.isnull()

d2 = df.values
d1 = nan_positions.values
isnan = np.isnan(d1)
all_nan_columns = np.all(d1, axis=0)
true_indices = [i for i, x in enumerate(all_nan_columns) if not x]
df = df.iloc[:, true_indices]
Columns = df.columns
d2 = df.values
d1 = nan_positions.values

d3 = list(d2[0])
if d2[0][-1]==0: 
    k = 1 
else: 
    k = 0
d3.append(0)
col1 = []
for i in range(len(d3)-1):
    if d3[i]!=d3[i+1]:
        col1.append(i)
col = []
a = 0
for j in col1:
    Col1 = []
    for i in range(a,j+1):
        
        Col1.append(i)
    a = j+1
    
    col.append(Col1)



col_name = []
col_id = []
    
for i in range(len(col)):
    
    data = d2[:,col[i]][np.unique(np.where(~d1[:,col[i]])[0])]
    data1 = d1[:,col[i]][np.unique(np.where(~d1[:,col[i]])[0])]


    
    for j in range(1,len(data)-1):
        L1 = []
        L2 = []
        for k in range(len(col[i])):
            if not data1[j][k]:
                if re.match(r'^\(.+\)$',data[j][k]):
                    item = re.findall(r'\w+', data[j][k])
                    l1,l2 = int(item[1]),int(item[2])
                    L1.append(l1)
                    L2.append(l2)
        l1 = min(L1)
        l2 = max(L2)
        
        


        I1 = []
        I2 = []
        for k in range(len(col[i])):
            if not data1[j][k]:
                if re.match(r'^\(.+\)$',data[j][k]):
                    item = re.findall(r'\w+', data[j][k])
                    item[1] = str(l1)
                    item[2] = str(l2)

            else:
                item = ['99999',l1,l2,'Unknown'+'_'+Columns[col[i]][k]+'_'+str(j)]
            result_a,result_b = gen_cols(item)
            I1.append(result_a)
            I2.append(result_b)

        u = 0
        for l in range(len(I2[u])):
            for k in range(len(I2)):
                col_id.append(I1[k][l])
                col_name.append(I2[k][l])
            u = u+1
    
    if '*' in data[-1][0]:
        reserve_int = int(data[-1][0][0:len(data[-1][0])-1])
        for k in range(reserve_int):
            for p in range(len(col[i])):
                item = ['99999',1,1,'Unknown'+'_'+Columns[col[i]][p]+'_'+str(k+len(data)-2)]
                result_a,result_b = gen_cols(item)
                col_name.append(result_b[0])
                col_id.append(result_a[0])





new_feature_id = col_id
new_feature_name = col_name

skip_rows = int(sys.argv[1])
nrows = int(sys.argv[2])

print("skip_rows: " + str(skip_rows) + ", nrows: " + str(nrows))
datafile=pd.read_csv('/home/shared/data/UKB/ukb_data/ukb670004.tab', sep='\\t', skiprows=range(1,skip_rows), nrows=nrows)




#datafile = pd.read_csv('Data_0601.csv')
old_features = datafile.columns.tolist()
ukb_data = datafile.values
nrows = len(ukb_data)
order = []
Order1 = []
Order2 = []
Data = []


for i in range(len(new_feature_id)):
    
    for j in range(0,len(old_features)):
        if new_feature_id[i] == old_features[j]:
            order.append(j)
            
            Order1.append(i)
            break
    if j == len(old_features)-1:
        Order2.append(i)
        Data.append(np.full(nrows,np.nan))
Data = np.array(Data).T

print(len(Order1)+len(Order2))

  # Define the chunk size (change according to your need)
Data2 = np.random.random((nrows,len(new_feature_id))).astype('O')



Data2[:,Order2]=Data

Data2[:,Order1] = ukb_data[:,order]
Data2 = pd.DataFrame(Data2,columns = new_feature_name)

Data2.to_csv('treatment_shell.csv',index = False)

str_list = Data2.columns.tolist()

iter_id = sys.argv[3]
output_path = os.path.join(OUTPUT_DIR, 'treatment_shell'+iter_id+'.csv')
print("output_path:" + output_path)
Data2.to_csv(output_path, index = False, header = False, mode='a')





