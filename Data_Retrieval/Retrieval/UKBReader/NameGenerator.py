# -*- coding: utf-8 -*-

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

import xlrd

class NameGenerator:
    def __init__(self, excel_name):
        """
        Initializes a NameGenerator object.
        @param excel_name: The name of the Excel file.
        """
        book = xlrd.open_workbook(excel_name)
        self.basic_sheet = book.sheet_by_name('basic-profile-834')
        self.diagnosis_sheet = book.sheet_by_name('diagnosis-13450')
        self.treatment_sheet = book.sheet_by_name('treatment-5680')
        self.result_sheet = book.sheet_by_name('result-512')
    
    def __prod(self, x):
        """
        Computes the product of a list of numbers.
        @param x: The list of numbers.
        @return: The product of the numbers.
        """
        if(type(x) == int):
            return x
        if(type(x) == list or type(x) == tuple):
            y = 1
            for i in x:
                y *= i
            return y
    
    def __is_empty(self, x):
        """
        Checks if a value is empty.
        @param x: The value to check.
        @return: True if the value is empty, False otherwise.
        """
        if(x == None):
            return True
        if(x == ''):
            return True
        if(x == '\s'):
            return True
        if(type(x) == list and len(x) == 0):
            return True
        return False

    def __is_unique(self, x):
        """
        Checks if all elements in a list are unique.
        @param x: The list to check.
        @return: True if all elements are unique, False otherwise.
        """
        store = dict()
        for i in x:
            if (i not in store):
                store[i] = 1
            else:
                print(i)
                return False
        return True
    
    def __transpose(self, x):
        """
        Transposes a 2D list.
        @param x: The 2D list to transpose.
        @return: The transposed list.
        """
        return list(map(list, zip(*x)))
    
    def __flatten(self, x):
        """
        Flattens a nested list.
        @param x: The nested list to flatten.
        @return: The flattened list.
        """
        y = list()
        for i in x:
            y.extend(i)
        return y
    
    def __is_available(self, x):
        """
        Checks if all elements in a list are available in a file.
        @param x: The list to check.
        @return: True if all elements are available, False otherwise.
        """
        with open('name.txt', 'r', encoding = 'utf-8') as f:
            strings = [i.strip() for i in f.readlines()]
        for (k, i) in enumerate(x):
            if('f.99999' in i):
                continue
            if(i not in strings):
                return False
        return True
    
    def run(self):
        """
        Runs the name generation process.
        @return: A tuple containing the generated names and indexes.
        """
        names = [None for i in range(4)]
        indexs = [None for i in range(4)]
        names[0], indexs[0] = self.generate_basic()
        names[1], indexs[1] = self.generate_diagnosis()
        names[2], indexs[2] = self.generate_treatment()
        names[3], indexs[3] = self.generate_result()
        
        titles = ['basic', 'diagnosis', 'treatment', 'result']
        for i in range(4):
            print('Names in {} is unique: {}'.format(titles[i], self.__is_unique(names[i])))
            print('Indexs in {} are in indexs of UKB: {}'.format(titles[i], self.__is_available(names[i])))
        return names, indexs
    
    def get_block_row(self, sheet):
        """
        Gets the ranges of blocks in a sheet based on the second-row values.
        @param sheet: The sheet to process.
        @return: A list of block ranges.
        """
        ranges = list()
        beg = 0
        for i in range(0, sheet.ncols-1):
            if(sheet.cell(1,i).value != sheet.cell(1, i+1).value):
                ranges.append([beg, i+1])
                beg = i+1
        ranges.append([beg, sheet.ncols])
        return ranges
    
    def get_size_row(self, sheet, cols):
        """
        Gets the size items from a sheet based on the last non-empty row in each column.
        @param sheet: The sheet to process.
        @param cols: The column range to consider.
        @return: A dictionary containing the size items.
        """
        last_index = sheet.nrows * 2
        for j in range(sheet.nrows - 1, 1, -1):
            flag = False
            for i in range(cols[0], cols[1]):
                value = sheet.cell(j, i).value
                if(not self.__is_empty(value)):
                    flag = True
            if(flag == True):
                last_index = j + 1
                break
        
        sizes = {i : 0 for i in range(2, last_index)}
        size_items = {i : None for i in range(2, last_index)}
        for i in range(cols[0], cols[1]):
            for j in range(2, last_index):
                value = sheet.cell(j, i).value
                if(not self.__is_empty(value)):
                    if('*' in value):
                        item = value.split('*')[0].strip()
                        if(sizes[j] < int(item)):
                            size_items[j] = [int(item), 1]
                            sizes[j] = int(item)
                    else:
                        items = value.split(',')
                        if(len(items) == 2):
                            sizes[j] = 1
                            size_items[j] = [1, 1]
                        else:
                            if(sizes[j] < int(items[1]) * int(items[2])):
                                size_items[j] = [int(items[1]), int(items[2])]
                                sizes[j] = int(items[1]) * int(items[2])
        return size_items
        
    def get_name_col(self, sheet, cols, size_item):
        """
        Gets the names and indexes for a column in a sheet based on the size items.
        @param sheet: The sheet to process.
        @param cols: The column range to consider.
        @param size_item: The size items for the column.
        @return: A tuple containing the names and indexes.
        """
        col_locs = dict()
        col_count = 0
        for i in list(size_item.keys()):
            col_locs[i] = col_count
            col_count += self.__prod(size_item[i])
        
        total_names = list()
        total_indexs = list()
        
        for i in range(cols[0], cols[1]):
            names = [None for i in range(col_count)]
            indexs = [None for i in range(col_count)]
            self.blank_number = 0
            father_name = sheet.cell(0, i).value
            for j in list(size_item.keys()):    
                col_loc = col_locs[j]
                value = sheet.cell(j, i).value
                true_size_1, true_size_2 = size_item[j]
                if(self.__is_empty(value)):
                    for k in range(col_loc, col_loc + (true_size_1 * true_size_2)):
                        names[k] = "{}/blank_{}".format(father_name, self.blank_number)
                        indexs[k] = 'f.{}.{}.{}'.format(99999, self.blank_number, 0)
                        self.blank_number += 1
                    continue
                if('*' in value):
                    for k in range(col_loc, col_loc + (true_size_1 * true_size_2)):
                        names[k] = "{}/blank_{}".format(father_name, self.blank_number)
                        indexs[k] = 'f.{}.{}.{}'.format(99999, self.blank_number, 0)
                        self.blank_number += 1
                    continue
                items = value.split(',')
                if(len(items) == 2):
                    names[col_loc] = '{}'.format(father_name)
                    indexs[col_loc] = 'f.eid'
                    continue
                father_index = int(items[0].split('(')[-1].strip())
                now_size_1 = int(items[1])
                now_size_2 = int(items[2])
                name = str(items[3].split(')')[0])
                for k1 in range(true_size_1):
                    for k2 in range(true_size_2):
                        names[col_loc + (k1 * true_size_2 + k2)] = '{}/{}_{}_{}'.format(father_name, name, k1, k2)
                        indexs[col_loc + (k1 * true_size_2 + k2)] = 'f.{}.{}.{}'.format(father_index, min(k1, now_size_1 - 1), min(k2, now_size_2 - 1))
            total_names.append(names)
            total_indexs.append(indexs)
        
        total_names = self.__flatten(self.__transpose(total_names))
        total_indexs = self.__flatten(self.__transpose(total_indexs))
        return total_names, total_indexs
                
    def generate_basic(self):
        """
        Generates the names and indexes for the basic profile sheet.
        @return: A tuple containing the names and indexes.
        """
        self.blank_number = 0
        basic_sheet = self.basic_sheet
        basic_ranges = self.get_block_row(basic_sheet)
        basic_total_names = list()
        basic_total_indexs = list()
        for (k, cols) in enumerate(basic_ranges):
            basic_size_item = self.get_size_row(basic_sheet, cols)
            basic_names, basic_indexs = self.get_name_col(basic_sheet, cols, basic_size_item)
            basic_total_names.extend(basic_names)
            basic_total_indexs.extend(basic_indexs)
        return basic_total_names, basic_total_indexs
    
    def generate_diagnosis(self):
        """
        Generates the names and indexes for the diagnosis sheet.
        @return: A tuple containing the names and indexes.
        """
        self.blank_number = 0
        diagnosis_sheet = self.diagnosis_sheet
        diagnosis_ranges = self.get_block_row(diagnosis_sheet)
        diagnosis_total_names = list()
        diagnosis_total_indexs = list()
        for (k, cols) in enumerate(diagnosis_ranges):
            diagnosis_size_item = self.get_size_row(diagnosis_sheet, cols)
            diagnosis_names, diagnosis_indexs = self.get_name_col(diagnosis_sheet, cols, diagnosis_size_item)
            diagnosis_total_names.extend(diagnosis_names)
            diagnosis_total_indexs.extend(diagnosis_indexs)
        return diagnosis_total_names, diagnosis_total_indexs
    
    def generate_treatment(self):
        """
        Generates the names and indexes for the treatment sheet.
        @return: A tuple containing the names and indexes.
        """
        self.blank_number = 0
        treatment_sheet = self.treatment_sheet
        treatment_ranges = self.get_block_row(treatment_sheet)
        treatment_total_names = list()
        treatment_total_indexs = list()
        for (k, cols) in enumerate(treatment_ranges):
            treatment_size_item = self.get_size_row(treatment_sheet, cols)
            treatment_names, treatment_indexs = self.get_name_col(treatment_sheet, cols, treatment_size_item)
            treatment_total_names.extend(treatment_names)
            treatment_total_indexs.extend(treatment_indexs)
        return treatment_total_names, treatment_total_indexs
    
    def generate_result(self):
        """
        Generates the names and indexes for the result sheet.
        @return: A tuple containing the names and indexes.
        """
        self.blank_number = 0
        result_sheet = self.result_sheet
        result_ranges = self.get_block_row(result_sheet)
        result_total_names = list()
        result_total_indexs = list()
        for (k, cols) in enumerate(result_ranges):
            result_size_item = self.get_size_row(result_sheet, cols)
            result_names, result_indexs = self.get_name_col(result_sheet, cols, result_size_item)
            result_total_names.extend(result_names)
            result_total_indexs.extend(result_indexs)
        return result_total_names, result_total_indexs
