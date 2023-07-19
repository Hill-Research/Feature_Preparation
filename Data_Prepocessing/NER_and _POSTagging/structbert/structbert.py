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

from modelscope.msdatasets import MsDataset
from modelscope.pipelines import pipeline
from modelscope.models import Model
from modelscope.utils.constant import Tasks
from modelscope.preprocessors import Preprocessor, TokenClassificationTransformersPreprocessor
from modelscope.trainers import build_trainer
import os

# SPECIFIED THE MODEL:
model = Model.from_pretrained('damo/nlp_structbert_part-of-speech_chinese-base')
tokenclas = pipeline(task=Tasks.token_classification, model=model)

# EVALUATION:
eval_dataset = MsDataset.load('data/1.txt')
input = MsDataset.load('data/1.txt')
diter = iter(input)
string = ""
while True:
        try:
            item = next(diter)["text"]
            seg_list = tokenclas(item.strip())["output"]
            for seg in seg_list:
                    string += seg['span'] + "\t" + seg['type'] + "\n"
            print(seg)
        except StopIteration:
            break
with open('res.txt', 'w+', encoding = 'utf-8') as f:
        f.write(string.strip()) 
