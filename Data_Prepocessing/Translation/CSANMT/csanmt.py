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

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.msdatasets import MsDataset
import os
import pandas as pd


pipeline_ins = pipeline(
    Tasks.translation, 'damo/nlp_csanmt_translation_en2zh')

#word-level translation:
files = os.listdir('datatrans')
count = 0
for file in files:
    input = MsDataset.load('datatrans/{}.txt'.format(count))
    diter = iter(input)
    string = ""
    while True:
        try:
            item = next(diter)["text"]
            result = pipeline_ins(item.strip())["translation"]
            string += item + "\t" + result + "\n"
        except StopIteration:
            break
    with open('results_csanmt/{}.txt'.format(count), 'w+', encoding = 'utf-8') as f:
        f.write(string.strip())
        count +=1
    print("File {} is done!".format(count))
   
#diagnosis test:
long_sent = MsDataset.load('datatrans/sent.txt')
output = ""
ite = iter(long_sent)
while True:
        try:
            item = next(ite)["text"]
            trans = pipeline_ins(item)["translation"]
            output += item + "\t --------" + trans + "\n"
        except StopIteration:
            break
with open('results_csanmt/long_sent.txt', 'w+', encoding = 'utf-8') as f:
    f.write(output)

#long sentence test:
long_sent = MsDataset.load('datatrans/longsent.txt')
output = ""
ite = iter(long_sent)
while True:
        try:
            item = next(ite)["text"]
            trans = pipeline_ins(item)["translation"]
            output += item + "\n ------------------------------" + trans + "\n"
        except StopIteration:
            break
with open('results_csanmt/sentences.txt', 'w+', encoding = 'utf-8') as f:
    f.write(output)
    
