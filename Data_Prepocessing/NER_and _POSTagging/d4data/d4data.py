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
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification
import os

# Load the pre-trained model
model_name = "d4data/biomedical-ner-all"
pipe = pipeline("ner", model="d4data/biomedical-ner-all", device=0)

if (not os.path.exists('results_d4data')):
    os.mkdir('results_d4data')
files = os.listdir('datatrans')
count = 0

# seg word test:
output = ""
for file in files:
    input = open('datatrans/'+file, 'r')
    for line in input:
        result = pipe(line.strip())
        for i in result:
            output += line+ "\t" +"word:"+ \
                i['word'] +"\t"+"entity:"+i['entity']+"\n"
    count += 1
    with open('results_d4data/{}.txt'.format(count), 'w+', encoding = 'utf-8') as f:
        f.write(output) 
        
# phrase test:
data = open('datatrans/sent.txt', 'r')
with open('results_d4data/phrase.txt', 'w+', encoding='utf-8') as f:
    for line in data:
        result = pipe(line.strip())
        for i in result:
            f.write(i['word'] + "\t" + i['entity'] + "\n")
            
# long sentence test:
longsent = open('datatrans/longsent.txt', 'r')
with open('results_d4data/sentence.txt', 'w+', encoding='utf-8') as f:
    for line in longsent:
        test = pipe(line.strip())
        for i in test:
            f.write(i['word'] + "\t" + i['entity'] + "\n")
# Evaluate the model's accuracy
# compare true_labels with predicted_labels
