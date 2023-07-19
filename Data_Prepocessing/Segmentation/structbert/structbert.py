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
