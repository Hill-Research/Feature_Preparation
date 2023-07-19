# -*- coding: utf-8 -*-

import re
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from DateProcesser import DateProcesser
import json

class DataPreprocesser:
    @classmethod
    def init_params(cls):
        cls.nan = -1
        cls.type_ = 'random'
        cls.fixed_col = [0, ]
        cls.__mkfile()
        DateProcesser.init_parameters()
        
    @classmethod
    def run(cls, title, file_path, save_path):
        cls.title = title
        cls.__readfile()
        cls.save_path = save_path.split('\\')[0]
        cls.__mkdir()
        data = pd.read_csv(file_path, sep=',', engine = 'python')
        columns = data.columns.to_numpy()
        values = data.values
        for k in range(np.shape(values)[1]):
            if k in cls.fixed_col:
                continue
            values[:, k] = cls.run_column(columns[k], values[:, k])
        
        # columns, values = cls.__flatten(columns, values)
        df = pd.DataFrame(values, columns = columns)
        df.to_csv(save_path, index = False, sep = ',', encoding='utf-8-sig')
        print(cls.string_search_dict)
        cls.__savefile()
        
    @classmethod
    def __is_empty(cls, x):
        if(x == None):
            return True
        if(x == ''):
            return True
        if(x == '\s'):
            return True
        if(pd.isnull(x)):
            return True
        if(type(x) == list and len(x) == 0):
            return True
        return False
    
    @classmethod
    def __is_alpha(cls, vector):
        for (i, item) in enumerate(vector):
            nonnumbers = re.findall('[A-Za-z]', str(item))
            if(len(nonnumbers) > 0):
                if(not cls.__is_empty(item)):
                    return True
            else:
                if((not cls.__is_number(item)) and cls.__is_empty(DateProcesser.blur_(item, level = "day"))):
                    if(not cls.__is_empty(item)):
                        return True
        return False
    
    @classmethod
    def __is_number(cls, x):
        if(type(x) in [float, int]):
            return True
        str_ = str(x).replace('\s','').replace('.','')
        flag1 = (not str_.isdigit())
        flag2 = (not (str_[0] == '-' and str_[1 :].isdigit()))
        if(flag1 and flag2):
            if(not cls.__is_empty(x)):
                return False
        return True
    
    @classmethod
    def __is_unique(cls, dic):
        alpha = 1.5
        if(sum(list(dic.values())) / len(list(dic.values())) < alpha):
            return True
        else:
            return False
    
    @classmethod
    def __get_number(cls, x):
        number = re.findall("([1-9]\\d*\\.\\d+|0\\.\\d+|[1-9]\\d*|0)", str(x))
        if(number != []):
            value = float(number[0])
        else:
            value = None
        return value
    
    @classmethod
    def __get_date(cls, x):
        y = DateProcesser.blur_(x, level = "day")
        return y
    
    @classmethod
    def __item_count(cls, vector):
        count_dic = dict()
        for item in vector:
            if(cls.__is_empty(item)):
                item = ''
            if(item not in count_dic):
                count_dic[item] = 1
            else:
                count_dic[item] += 1
        return count_dic
    
    @classmethod
    def __one_hot(cls, item, sub_list):
        return tuple(['1' if i==item else '0' for i in sub_list])
    
    @classmethod
    def __mkdir(cls):
        save_path = cls.save_path
        if(not os.path.exists(save_path)):
            os.mkdir(save_path)
            
        titles = ['basic', 'diagnosis', 'treatment', 'result']
        for title in titles:
            if(not os.path.exists(os.path.join(save_path, title))):
                os.mkdir(os.path.join(save_path, title))

    @classmethod
    def __mkfile(cls):
        titles = ['basic', 'diagnosis', 'result', 'treatment']
        for title in titles:
            dic = dict()
            with open('{}_string_search_dict.json'.format(title), 'w+', encoding = 'utf-8') as f:
                json.dump(dic, f)
    
    @classmethod
    def __readfile(cls):
        with open('{}_string_search_dict.json'.format(cls.title), 'r', encoding = 'utf-8') as f:
            cls.string_search_dict = json.load(f)
    
    @classmethod
    def __savefile(cls):
        with open('{}_string_search_dict.json'.format(cls.title), 'w+', encoding = 'utf-8') as f:
            json.dump(cls.string_search_dict, f)
            
    @classmethod
    def __flatten(cls, columns, values):
        flatten_columns = list()
        flatten_indexs = list()
        count = values.shape[1]
        for (k, item) in enumerate(columns):
            print(k)
            if(type(values[0, k]) == list):
                for i in range(len(values[0, k])):
                    new_key = '{}_{}'.format(item, i)
                    new_col = [values[j, k][i] for j in range(values.shape[0])]
                    flatten_columns.append(new_key)
                    values = np.insert(values, count, new_col, axis = 1)
                    flatten_indexs.append(count)
                    count += 1
            else:
                flatten_columns.append(item)
                flatten_indexs.append(k)
        flatten_values = values[:, np.array(flatten_indexs)]
        return flatten_columns, flatten_values
    
    @classmethod
    def generate_all_blank(cls, vector):
        for (i, item) in enumerate(vector):
            vector[i] = cls.nan
        return vector
    
    @classmethod
    def generate_string(cls, name, vector, count_dic):
        if(name not in cls.string_search_dict):
            cls.string_search_dict[name] = list()
        keys = list()
        values = list()
        print(vector, count_dic)
        for i in count_dic:
            if(i == ''):
                continue
            keys.append(i)
            values.append(count_dic[i])
        
        if(cls.type_ == 'random'):
            probs = [i / sum(values) for i in values]
            for (i, item) in enumerate(vector):
                if(cls.__is_empty(item)):
                    vector[i] = np.random.choice(keys, p = probs)
        if(cls.type_ == 'maximum'):
            indexs = np.where(values == np.max(values))[0]
            for (i, item) in enumerate(vector):
                if(cls.__is_empty(item)):
                    vector[i] = keys[int(indexs[0])]
        
        for key in keys:
            if(key not in cls.string_search_dict[name]):
                cls.string_search_dict[name].append(key)
        
        for (i, item) in enumerate(vector):
            vector[i] = ','.join(cls.__one_hot(item, cls.string_search_dict[name]))
        
        return vector
    
    @classmethod
    def generate_some_blank(cls, vector, count_dic):
        keys = list()
        values = list()
        for i in count_dic:
            if(i == ''):
                continue
            keys.append(i)
            values.append(count_dic[i])
        
        if(cls.type_ == 'random'):
            probs = [i / sum(values) for i in values]
            for (i, item) in enumerate(vector):
                if(cls.__is_empty(item)):
                    vector[i] = np.random.choice(keys, p = probs)
        if(cls.type_ == 'maximum'):
            indexs = np.where(values == np.max(values))[0]
            for (i, item) in enumerate(vector):
                if(cls.__is_empty(item)):
                    vector[i] = keys[int(indexs[0])]
        
        for (i, item) in enumerate(vector):
            if(cls.__is_number(item)):
                vector[i] = cls.__get_number(item)
            else:
                vector[i] = cls.__get_date(item)
        return vector
    
    @classmethod
    def run_column(cls, name, vector):
        count_dic = cls.__item_count(vector)
        if('' not in count_dic or count_dic[''] < 500):
            if(cls.__is_alpha(vector)):
                print(count_dic, cls.__is_alpha(vector))
        type_ = -1
        if('' in count_dic and count_dic[''] == len(vector)):
            type_ = 0
        else:
            if('' not in count_dic):
                if(cls.__is_alpha(vector)):
                    if(cls.__is_unique(count_dic)):
                        type_ = 1
                    else:
                        type_ = 2
                else:
                    type_ = 1
            else:
                if(cls.__is_alpha(vector)):
                    if(cls.__is_unique(count_dic)):
                        type_ = 1
                    else:
                        type_ = 2
                else:
                    type_ = 3
        
        if(type_ == 0):
            vector = cls.generate_all_blank(vector)
        if(type_ == 1):
            vector = vector.copy()
        if(type_ == 2):
            vector = cls.generate_string(name, vector, count_dic)
        if(type_ == 3):
            vector = cls.generate_some_blank(vector, count_dic)
        return vector

file_father_path = 'extraction_data'
save_father_path = 'preprocessed_data'

titles = ['basic', 'diagnosis', 'result', 'treatment']

DataPreprocesser.init_params()
for title in titles:
    file_names = os.listdir(os.path.join(file_father_path, title))
    max_counts = len(file_names)   
    with tqdm(total = max_counts) as pbar:
        pbar.set_description('Preprocess data for {}.'.format(title))
        for file_name in file_names:
            file_path = os.path.join(file_father_path, title, file_name)
            save_path = os.path.join(save_father_path, title, file_name)
            DataPreprocesser.run(title, file_path, save_path)
            pbar.update(1)