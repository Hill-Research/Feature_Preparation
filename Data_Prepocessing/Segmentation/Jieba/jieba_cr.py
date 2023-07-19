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

import os
import jieba

names=os.listdir('criteria')

count = 0
if(not os.path.exists('semi-labeled-data')):
    os.mkdir('semi-labeled-data')

print(len(names))
for name in names:
    path=os.path.join('criteria', name)
    with open(path, 'r', encoding = 'utf-8') as f:
        text = f.read()
    lists = ['<', '>', '≤', '≥']
    if('<' in text or '>' in text, '≤' in text or '≥' in text):
        text=text.strip()
        seg_list=jieba.cut(text, cut_all=False)
        flag = 0
        string = ""
        for item in seg_list:
            if(item == ' '):
                continue
            if(item in lists):
                flag = 3
            if(flag>0 and item not in [' ', '\n', '\t', '.', ',', ';', '//']):
                flag -= 1
                string += "{}\t{}\n".format(item, 'NUMBER')
            else:
                if(item in ['\r', '\n', '\t']):
                    string += "{}\t{}\n".format('.', 'ELSE')
                else:
                    string += "{}\t{}\n".format(item, 'ELSE')
        with open('semi-labeled-data/{}.txt'.format(count), 'w+', encoding = 'utf-8') as g:
            g.write(string.strip())
            count += 1
print(count)
