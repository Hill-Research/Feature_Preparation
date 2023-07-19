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

# 指定需要提取的列
cols = ['f.40010.0.0', 'f.12653.2.0', 'f.12653.2.1', 'f.12653.2.2', 'f.12653.2.3', 'f.12653.2.4', 'f.12653.2.5', 'f.12653.2.6', 'f.12653.2.7', 'f.12653.2.8', 'f.12653.2.9', 'f.12653.2.10', 'f.12653.2.11', 'f.12653.2.12', 'f.12653.2.13', 'f.12653.2.14', 'f.12653.3.0', 'f.12653.3.1', 'f.12653.3.2', 'f.12653.3.3', 'f.12653.3.4', 'f.12653.3.5', 'f.12653.3.6', 'f.12653.3.7', 'f.12653.3.8', 'f.12653.3.9', 'f.12653.3.10', 'f.12653.3.11', 'f.12653.3.12', 'f.12653.3.13', 'f.12653.3.14']

# 循环读取每列并存为csv
for col_name in cols:
    # 读取指定列
    df = pd.read_csv('ukb670004.tab', sep='\t', usecols=[col_name])
    
    # 删除包含缺失值的任何行
    df_cleaned = df.dropna()
    
    # 将结果保存为一个CSV文件
    output_file_name = f"{col_name}.csv"
    df_cleaned.to_csv(output_file_name, index=False)

