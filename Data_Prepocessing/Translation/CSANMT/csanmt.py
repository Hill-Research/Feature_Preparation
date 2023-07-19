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
    
