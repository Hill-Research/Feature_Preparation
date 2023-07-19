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
from modelscope.preprocessors import Preprocessor, TokenClassificationTransformersPreprocessor
from modelscope.trainers import build_trainer
from modelscope.utils.constant import Tasks
import os


#default model:
word_segmentation = pipeline("word-segmentation")

# SPECIFIED THE MODEL:
model = Model.from_pretrained('damo/nlp_structbert_word-segmentation_chinese-base')
wordseg = pipeline(task=Tasks.word_segmentation, model=model)


if(not os.path.exists('results_bert')):
    os.mkdir('results_bert')
files = os.listdir('data')
count = 0
for file in files:
    # DATASET:
    input = MsDataset.load('data/'+file)
    diter = iter(input)
    string = ""
    while True:
        try:
            item = next(diter)["text"]
            seg_list = wordseg(item.strip())["output"]
            for seg in seg_list:
                if (seg in [' ', ',', '\n', '\t', ';', '/', '//', '.', '。', '《', '》', '〈', '〉']):
                    continue
                else:
                    string += seg + "\n"
        except StopIteration:
            break
    with open('results_bert/{}.txt'.format(count), 'w+', encoding = 'utf-8') as f:
        f.write(string.strip())
        count +=1
    print("File {} is done!".format(count))
