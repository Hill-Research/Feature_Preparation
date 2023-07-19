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
OUTPUT_DIR='basic_out'
file_path = r'CSV-UKB-Features-Design_basic_profile.csv'
df = pd.read_csv(file_path)
nan_positions = df.isnull()

d2 = df.values
d1 = nan_positions.values
isnan = np.isnan(d1)
all_nan_columns = np.all(d1, axis=0)
true_indices = [i for i, x in enumerate(all_nan_columns) if not x]
df = df.iloc[:, true_indices]



Set = []
for i in range(len(df.columns.tolist())):
    item = df.columns.tolist()[i].split('_')[0]
    if item not in Set:
        Set.append(item)
Columns = df.columns.tolist()
col = [] 
for i in range(len(Set)):
    col1 = []
    for j in range(len(df.columns.tolist())):
        if df.columns.tolist()[j].split('_')[0] == Set[i]:
            col1.append(j)
    col.append(col1)
col_name = []
col_id = []
for i in range(1,len(col)):
    data = d2[:,col[i]][np.unique(np.where(~d1[:,col[i]])[0])]
    #data = data[1:len(data)]
    data1 = d1[:,col[i]][np.unique(np.where(~d1[:,col[i]])[0])]
    #data1 = data1[1:len(data1)]

    #data = data[1:len(data)-1]
    #data1 = data1[1:len(data1)-1]

    if len(col[i]) == 1:
        for j in range(1,len(data)):
            if re.match(r'^\(.+\)$',data[j][0]):
                item1 = re.findall(r'\w+', data[j][0])
                result_a,result_b = gen_cols(item1)
                for a in result_b:
                    col_name.append(a)
                for a in result_a:
                    col_id.append(a)
            elif '*' in data[j][0]:
                reserve_int = int(data[j][0][0:len(data[j][0])-1])
                for j in range(len(data)-1,len(data)-1+reserve_int):
                    col_id.append(Columns[col[i][0]]+'_'+'Unknow_name'+str(j))
                    col_name.append(Columns[col[i][0]]+'_'+'Unknow_name'+str(j))
                    

    if len(col[i])==3:
        if len(data)>2:

            for j in range(1,len(data)-1):
                if re.match(r'^\(.+\)$',data[j][1]):
                    item1 = re.findall(r'\w+', data[j][1])
                if data1[j][0]:
                    type = Columns[col[i][0]]+'_'+'Unknow_name'+str(j)
                else:
                    type = data[j][0]
                if data1[j][2]:
                    item2 = ['99999',item1[1],'1',type+'_'+'Unknown_Date']

                else:
                    item2 = re.findall(r'\w+', data[j][2])
                result_a,result_b = gen_cols(item1)
                result_b = np.array(result_b).reshape((int(item1[1]),int(item1[2])))
                date_a,date_b = gen_cols(item2) 
                k = 0
                for a in range(int(item1[1])):
                    
                    for b in range(int(item1[2])):
                        col_name.append(type+'_'+str(k))
                        col_name.append(result_b[a][b])
                        col_name.append(date_b[a])
                        
                        col_id.append(type+'_'+str(k))
                        col_id.append(result_a[a][b])
                        col_id.append(date_a[a])
                        k = k+1
        if '*' in data[-1][0]:
            reserve_int = int(data[-1][0][0:len(data[-1])-1])
            for j in range(len(data)-1,len(data)-1+reserve_int):
                col_name.append(Columns[col[i][0]]+'_'+'Unknow_name'+str(j))
                col_id.append(Columns[col[i][0]]+'_'+'Unknow_name'+str(j))
                result_a,result_b = gen_cols(['99999','1','1','Unknow_name'+str(j)])
                date_a,date_b = gen_cols(['99999','1','1','Unknow_date'+str(j)])
                for a in result_b:
                    col_name.append(a)
                for b in date_b:
                    col_name.append(b)
                for a in result_a:
                    col_id.append(a)
                for b in date_a:
                    col_id.append(b)



new_feature_id = col_id
new_feature_name = col_name

skip_rows = int(sys.argv[1])
nrows = int(sys.argv[2])

print("skip_rows: " + str(skip_rows) + ", nrows: " + str(nrows))
datafile=pd.read_csv('/home/shared/data/UKB/ukb_data/ukb670004.tab', sep='\\t', skiprows=range(1,skip_rows), nrows=nrows)
#df_list.get_chunk(chunksize)



old_features = datafile.columns.tolist()
ukb_data = datafile.values

order = []
Order1 = []
Order2 = []
Data = []
k=0

for i in range(len(new_feature_id)):
    
    for j in range(0,len(old_features)):
        if new_feature_id[i] == old_features[j]:
            order.append(j)
            
            Order1.append(k)
            break
    if j == len(old_features)-1:
        Order2.append(k)
        Data.append(np.full(nrows,np.nan))
    k = k+1
print(len(Order1)+len(Order2))
Data2 = np.random.random((nrows,len(new_feature_id)))
Data = np.array(Data).reshape(Data2[:,Order2].shape)

Data2[:,Order2]=Data
Data2[:,Order1] = ukb_data[:,order]
Data2 = pd.DataFrame(Data2,columns = new_feature_name)

iter_id = sys.argv[3]
output_path = os.path.join(OUTPUT_DIR, 'basic_shell'+iter_id+'.csv')
print("output_path:" + output_path)
Data2.to_csv(output_path, index = False, header = False, mode='a')


