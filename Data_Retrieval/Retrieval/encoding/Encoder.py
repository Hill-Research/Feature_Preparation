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


class Encoder:
    def __init__(self, path):
        """
        Initialize the Encoder.
        @param path: specifies the CSV file which needs to be encoded
        """
        df_raw = pd.read_csv(path)
        df_target = df_raw.loc[:, lambda d: d.columns.str.contains('ICD10')]  # 只提取需要处理的column
        self.df = df_target.fillna("-1")  # Fill All NA as -1

    def genEncodeDict(self):
        """
        Generate encoding dictionary from the given dataframe.
        @todo 1: need to write the encoding dictionary into a separate file, and only generate new encoding rules when the original dict cannot handle new data fields
        @return: the encoding dictionary
        """
        unique_set = set()
        for col in self.df.columns:
            unique_set = unique_set.union(set(self.df[col].unique().tolist()))

        unique_set.remove('-1')
        unique_list = list(unique_set)

        unique_dict = dict()
        for i in range(1, len(unique_list) + 1):
            unique_dict[unique_list[i - 1]] = i
        unique_dict['-1'] = -1

        return unique_dict

    def encode(self):
        """
        Encode the dataframe data fields based on the dictionary.
        @todo we are assuming that each column in the dataframe should be encoded, which is not always true
        @return: encoded dataframe
        """
        encodingDict = self.genEncodeDict()
        for col in self.df.columns:
            self.df[col] = self.df[col].map(lambda cell: encodingDict[cell])

    def dump(self, output_path):
        """
        Dump the encoded dataframe into output file
        @param output_path: the file handler to the output file
        @return: None
        """
        self.df.to_csv(output_path)
