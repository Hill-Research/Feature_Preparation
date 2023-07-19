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
