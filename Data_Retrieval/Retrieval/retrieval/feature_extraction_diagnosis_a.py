#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re
import sys
import numpy as np


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
file_path = r'CSV-UKB-Features-Design_diagnosis.csv'
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

def GC3(data,data1,C,j):
    if C[0].split('_')[0]=='genetic':
        h = 'Unknown_confidence'
    else:
        h = 'Unknown_date'
    col_name = []
    col_id = []
    if data1[0]:
        type = C[0]+'_'+'Unknow'+str(j)
    else:
        type = data[0]
    item1 = re.findall(r'\w+', data[1])
    if data1[2]:
        item2 = ['99999',item1[1],'1',type+'_'+h]

    else:
        item2 = re.findall(r'\w+', data[2])
    if type == item1[3]:
        type = type+'_'+'type'
        item1[3] = item1[3]+'_'+'result'
    result_a,result_b = gen_cols(item1)
    date_a,date_b = gen_cols(item2) 
    
    result_b = np.array(result_b).reshape((int(item1[1]),int(item1[2])))
    result_a = np.array(result_a).reshape((int(item1[1]),int(item1[2])))
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
    return col_id,col_name

def GC2(data,data1,C,j):
    col_name = []
    col_id = []
    
    item1 = re.findall(r'\w+', data[0])
    if data1[1]:
        item2 = ['99999',item1[1],'1',C[0]+'_'+'Unknown_Date']

    else:
        item2 = re.findall(r'\w+', data[1])
    
    result_a,result_b = gen_cols(item1)
    date_a,date_b = gen_cols(item2) 
    result_b = np.array(result_b).reshape((int(item1[1]),int(item1[2])))
    result_a = np.array(result_a).reshape((int(item1[1]),int(item1[2])))
    for a in range(int(item1[1])):
        for b in range(int(item1[2])):
            
            col_name.append(result_b[a][b])
            col_name.append(date_b[a])
            
            col_id.append(result_a[a][b])
            col_id.append(date_a[a])
    return col_id,col_name


def star3(reserve_int,data,C):
    if C[0]=='genetic':
        h = 'Unknown_confidence'
    else:
        h = 'Unknown_date'
    col_id = []
    col_name = []
    for j in range(len(data)-1,len(data)-1+reserve_int):
        col_name.append(C[0]+'_'+'Unknow_name'+str(j))
        col_id.append(C[0]+'_'+'Unknow_name'+str(j))
        result_a,result_b = gen_cols(['99999','1','1',C[0]+'_'+'Unknow_result'+str(j)])
        date_a,date_b = gen_cols(['99999','1','1',C[0]+'_'+h+str(j)])
        col_name.append(result_b[0])
        col_name.append(date_b[0])
        
        col_id.append(result_a[0])
        col_id.append(date_a[0])
    return col_id,col_name
def star2(reserve_int,data,C):
    col_id = []
    col_name = []
    for j in range(len(data)-1,len(data)-1+reserve_int):
        result_a,result_b = gen_cols(['99999','1','1',C[0]+'_'+'Unknow_result'+str(j)])
        date_a,date_b = gen_cols(['99999','1','1',C[0]+'_'+'Unknow_date'+str(j)])
        col_name.append(result_b[0])
        col_name.append(date_b[0])
        
        col_id.append(result_a[0])
        col_id.append(date_a[0])
    return col_id,col_name
data = d2[:,col[-1]][np.unique(np.where(~d1[:,col[-1]])[0])]
def star_res(reserve_int,data,C):
    col_id = []
    col_name = []
    
    
    for j in range(len(data)-1,len(data)-1+reserve_int):
        col_name.append(C[0]+'_'+str(j))
        col_id.append(C[0]+'_'+str(j))
    return col_id,col_name
#star_res(100,data,Columns[col[-1]])



col_id = []
col_name = []
for i in range(len(col)):
    
    
    
    data = d2[:,col[i]][np.unique(np.where(~d1[:,col[i]])[0])]
    data1 = d1[:,col[i]][np.unique(np.where(~d1[:,col[i]])[0])]
    if i == 1:
        data = data[0:63]
    reserve_int = int(data[-1][0][0:len(data[-1][0])-1])
    C = Columns[col[i]][0].split('_')
    if i == len(col)-1:
        #reserve_int = int(data[-1][0:len(data[-1])-1])
        a1,b1 = star_res(reserve_int,data,C)

    if len(data)>2:
        for j in range(1,len(data)-1):
            if len(col[i])==3:
                a,b = GC3(data[j],data1[j],C,j)
            if len(col[i]) == 2:
                a,b = GC2(data[j],data1[j],C,j)

            for k in range(len(a)):
                col_id.append(a[k])
                col_name.append(b[k])
    if len(col[i])==3:
        a1,b1 = star3(reserve_int,data,C)
    if len(col[i]) == 2:
        a1,b1 = star2(reserve_int,data,C)
    for k in range(len(a1)):
        col_id.append(a1[k])
        col_name.append(b1[k])
  
    
    
print(len(col_id),len(col_name))


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

print(len(Order1)+len(Order2))

Data2 = np.random.random((nrows,len(new_feature_id))).astype('O')

Data = np.array(Data).T

Data2[:,Order2]=Data

Data2[:,Order1] = ukb_data[:,order]
Data2 = pd.DataFrame(Data2,columns = new_feature_name)

Data2.to_csv('diagnosis_shell.csv',index = False)



# str_list = Data2.columns.tolist()

# with open('Columns_name_0602_diagnosis.txt', 'w') as file:
#     # Write each string followed by a newline character
#     for string in str_list:
#         file.write(string + '\n')





















