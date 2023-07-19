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

# import matplotlib.pyplot as plt
import jieba
import os
import xlwt

if(not os.path.exists('ukb_train_data')):
    os.mkdir('ukb_train_data')
with open('ukb_data/text_data/f.40010.0.0.csv', 'r', encoding = 'utf-8') as f:
    text_list = [i for i in f.readlines()]

lengths = [len(text) for text in text_list]

# fig=plt.figure(figsize=(6,6))
# ax=fig.add_subplot(111)
# ax.hist(lengths, bins=50)
# plt.show()

count=0
for text in text_list:
    if (len(text)>200):
        text=text.strip()
        seg_list=jieba.cut(text, cut_all=False)
        seg_list=[i for i in seg_list if i!=' ']
        
        book=xlwt.Workbook(encoding='utf-8')
        sheet=book.add_sheet('Sheet 1')
        sheet.write(0,1,'bod')
        sheet.write(0,2,'dis')
        sheet.write(0,3,'dru')
        sheet.write(0,4,'seg')

        for (i,item) in enumerate(seg_list):
            sheet.write(i+1,0,item)
        book.save('ukb_train_data/{}.xls'.format(count))