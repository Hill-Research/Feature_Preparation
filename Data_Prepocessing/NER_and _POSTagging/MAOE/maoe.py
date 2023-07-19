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
from adaseq import pipelines

pipeline_ins = pipeline(
    Tasks.named_entity_recognition, 'damo/nlp_maoe_named-entity-recognition_chinese-base-general'
)

if(not os.path.exists('results_maoe')):
    os.mkdir('results_maoe')
files = os.listdir('data')
count = 0
for file in files:
    input = MsDataset.load('data/'+file)
    diter = iter(input)
    string = ""
    while True:
        try:
            item = next(diter)["text"]
            seg_list = pipeline_ins(item.strip())["output"]
            for seg in seg_list:
                string += seg['span'] + "\t" + seg['type'] + "\n"
        except StopIteration:
            break
    with open('results_maoe/{}.txt'.format(count), 'w+', encoding = 'utf-8') as f:
        f.write(string.strip())
        count +=1
    print("File {} is done!".format(count))
