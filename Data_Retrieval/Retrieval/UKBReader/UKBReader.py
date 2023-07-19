# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
from NameGenerator import NameGenerator
from tqdm import tqdm
import time

class UKBReader:
    def __init__(self, ukb_file, save_path):
        """
        Initialize the UKBReader object.

        Args:
            ukb_file (str): Path to the UKB data file.
            save_path (str): Path to the directory where the extracted data will be saved.
        """
        self.ukb_file = ukb_file
        self.chunksize = 500
        self.save_path = save_path
        
    def __if_index_file(self, vector):
        """
        Check if the index file exists and create it if not.

        Args:
            vector (list): List of feature names.
        """
        if(not os.path.exists('name.txt')):
            string = ''
            with open('name.txt', 'w+', encoding = 'utf-8') as f:
                for i in vector:
                    string += '{}\n'.format(i)
                f.write(string.strip())

    def __mkdir(self):
        """
        Create necessary directories for saving the extracted data.
        """
        save_path = self.save_path
        if(not os.path.exists(save_path)):
            os.mkdir(save_path)
            
        titles = ['basic', 'diagnosis', 'treatment', 'result']
        for title in titles:
            if(not os.path.exists(os.path.join(save_path, title))):
                os.mkdir(os.path.join(save_path, title))
    
    def run(self):
        """
        Run the UKBReader to extract data from the UKB file and save it to separate CSV files.
        """
        self.__mkdir()
        datafile_iterator = pd.read_csv(self.ukb_file, sep=',', engine = 'python', chunksize = self.chunksize)
        # self.__if_index_file(datafile.columns.tolist())
        feature_names, feature_indexs = self.read_Feature_name_index()
        UKB_index = self.read_UKB_index()
        titles = ['basic', 'diagnosis', 'treatment', 'result']
        
        # max_counts = (502394 // self.chunksize)
        max_counts = (1000 // self.chunksize)
        
        with tqdm(total = max_counts * 4) as pbar:
            pbar.set_description('Extracting data:')
            for (j, datafile) in enumerate(datafile_iterator):
                for (i, (feature_name, feature_index)) in enumerate(zip(feature_names, feature_indexs)):
                    search_dict = self.read_locate_index(feature_index, UKB_index)
                    file_name = '{}/{}_{}-{}.csv'.format(titles[i], titles[i], j * self.chunksize, j * self.chunksize + datafile.shape[0])
                    self.read_patch(datafile, feature_name, feature_index, search_dict, file_name)
                    pbar.update(1)
    
    def read_locate_index(self, list1, list2):
        """
        Create a dictionary to map feature indices to their corresponding column positions in the data.

        Args:
            list1 (list): List of feature indices.
            list2 (list): List of UKB index.

        Returns:
            store (dict): Dictionary mapping feature indices to column positions.
        """
        store = dict()
        for i in list1:
            store[i] = len(list2)
            
        for (k,j) in enumerate(list2):
            store[j] = k
        return store
    
    def read_Feature_name_index(self):
        """
        Read the feature names and indices from a CSV file.

        Returns:
            names (list): List of feature names.
            indexs (list): List of feature indices.
        """
        csv_name = NameGenerator('CSV_UKB_Feature_Design_final_version2_6262023.xls')
        names, indexs = csv_name.run()
        return names, indexs

    def read_UKB_index(self):
        """
        Read the UKB index from the index file.

        Returns:
            strings (list): List of UKB index.
        """
        with open('name.txt', 'r', encoding = 'utf-8') as f:
            strings = [i.strip() for i in f.readlines()]
        return strings
    
    def read_patch(self, datafile, feature_name, feature_index, search_dict, name):
        """
        Read a patch of data and save it to a CSV file.

        Args:
            datafile (DataFrame): Dataframe containing the data.
            feature_name (list): List of feature names.
            feature_index (list): List of feature indices.
            search_dict (dict): Dictionary mapping feature indices to column positions.
            name (str): Name of the CSV file to save the data.
        """
        ukb_data = datafile.values
        # print(np.ones(np.shape(ukb_data)[0],1))
        none_vector = [None for i in range(np.shape(ukb_data)[0])]
        ukb_data = np.insert(ukb_data, np.shape(ukb_data)[1], none_vector, axis = 1)
        searched_indexs = list()
        for index in feature_index:
            searched_indexs.append(search_dict[index])
        
        keys = feature_name
        values = ukb_data[:, np.array(searched_indexs)]
        df = pd.DataFrame(values, columns = keys)
        df.to_csv(os.path.join(self.save_path, name))


beg_time = time.time()
ukb_data = '0-1000.csv'
save_path = 'extraction_data'
reader = UKBReader(ukb_data, save_path)
reader.run()
print('Final time cost: {} min'.format((time.time() - beg_time) // 60))
