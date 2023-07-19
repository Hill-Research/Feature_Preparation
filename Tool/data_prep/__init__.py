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
