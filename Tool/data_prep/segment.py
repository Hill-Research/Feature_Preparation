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

import os

# segmentation - Jieba model
def seg_jieba(file):
# TODO - add saving delimiters
# TODO - add input formats
    import jieba
    # /path/to/files
    if os.path.isdir(file):
        if(not os.path.exists('seg_result')):
            os.mkdir('seg_result')
        # Open all txt files in the specified directory
        count = 0
        for file_name in os.listdir(file):
            if file_name.endswith('.txt'):
                path = os.path.join(file, file_name)
                with open(path, 'r', encoding = 'utf-8') as f:
                    text = f.read()
                    text = text.strip()
                    seg_list = jieba.cut(text, cut_all=False)
                    output = ""
                    name = file_name.split("/")[-1].split(".")[0]
                    for item in seg_list:
                        # TODO - ignore puctuations
                        if(item in [' ', ',', '\n', '\t']):
                            continue
                        else:
                            output += "{}\n".format(item.strip())
                    with open('seg_result/{}_result.txt'.format(name), 'w+', encoding = 'utf-8') as g:
                        g.write(output.strip())
                        count += 1
                        # show progress
                        print("File {} segmented with Jieba.".format(file_name))
    # single file name
    elif os.path.isfile(file) and file.endswith('.txt'):
        if(not os.path.exists('seg_result')):
            os.mkdir('seg_result')
        file_name = file.split("/")[-1].split(".")[0]
        with open(file, 'r') as f:
            text = f.read()
            text = text.strip()
            seg_list = jieba.cut(text, cut_all=False)
            output = ""
            for item in seg_list:
                if(item in [' ', ',', '\n', '\t']):
                    continue
                else:
                    output += "{}\n".format(item.strip())
            with open('seg_result/{}_result.txt'.format(file_name), 'w+', encoding = 'utf-8') as g:
                g.write(output.strip())
        print("File {} segmented with Jieba.".format(file_name))
    else:
        print('Invalid file path or type')

def seg2(file):
    import nltk
    # Load custom dictionary with weights
    with open('seg_dict.txt', 'r') as f:
        custom_dictionary = {}
        for line in f:
            line = line.strip().split()
            try:
                weight = int(line[-1])
            except ValueError:
                weight = 1
            custom_dictionary[tuple(line[:-1])] = weight
    # /path/to/files
    if os.path.isdir(file):
        if(not os.path.exists('seg_result')):
            os.mkdir('seg_result')
        # Open all txt files in the specified directory
        count = 0
        for file_name in os.listdir(file):
            if file_name.endswith('.txt'):
                path = os.path.join(file, file_name)
                name = file_name.split("/")[-1].split(".")[0]
                with open(path, 'r', encoding = 'utf-8') as f:
                    text = f.read()
                    text = text.strip()
                    # Tokenize text using NLTK's word tokenizer
                    tokens = nltk.word_tokenize(text)
                    # Initialize multi-word expression tokenizer with custom dictionary
                    tokenizer = nltk.MWETokenizer(list(custom_dictionary.keys()))
                    # Tokenize text and join multi-word expressions
                    tokens = tokenizer.tokenize(tokens)
                    # Replace underscores with spaces in tokens
                    tokens = [token.replace('_', ' ') for token in tokens]
                    with open('seg_result/{}_result.txt'.format(name), 'w+', encoding = 'utf-8') as g:
                        g.write('\n'.join(tokens).strip())
                        count += 1
                        # show progress
                        print("File {} segmented with nltk according to 'seg_dict.txt'.".format(file_name))
    # single file name
    elif os.path.isfile(file) and file.endswith('.txt'):
        if(not os.path.exists('seg_result')):
            os.mkdir('seg_result')
        file_name = file.split("/")[-1].split(".")[0]
        with open(file, 'r', encoding = 'utf-8') as f:
            text = f.read()
            text = text.strip()
            # Tokenize text using NLTK's word tokenizer
            tokens = nltk.word_tokenize(text)
            # Initialize multi-word expression tokenizer with custom dictionary
            tokenizer = nltk.MWETokenizer(list(custom_dictionary.keys()))
            # Tokenize text and join multi-word expressions
            tokens = tokenizer.tokenize(tokens)
            # Replace underscores with spaces in tokens
            tokens = [token.replace('_', ' ') for token in tokens]
            with open('seg_result/{}_result.txt'.format(file_name), 'w+', encoding = 'utf-8') as g:
                g.write('\n'.join(tokens).strip())
        print("File {} segmented with nltk according to 'seg_dict.txt'.".format(file_name))
    else:
        print('Invalid file path or type')

