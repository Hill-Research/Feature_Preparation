from .segment import seg_jieba, seg2
from .tag import tag1, tag2
from .translate import trans,trans_csv, trans_google, trans_google_csv
from .delete import dele, dele2

# Define dictionaries to map the task names to the appropriate functions and models
tagging_models = {'number': tag1, 'tag2': tag2}
segmentation_models = {'seg': seg_jieba, 'eng_dict': seg2}
translation_models = {'trans': trans, 'google': trans_google, 'google_csv':trans_google_csv, 'trans_csv': trans_csv}
delete_models = {'delete': dele, 'del_after_seg': dele2}

def process(text, task, model):
    models = {'tag': tagging_models, 
              'segment': segmentation_models,
              'translate': translation_models,
              'delete': delete_models
              }
    if task not in models:
        raise ValueError('Task not supported: {}'.format(task))
    try:
        return models[task][model](text)
    except KeyError:
        raise ValueError('{} model not supported for task {}: {}'.format(model, task, models[task].keys()))
