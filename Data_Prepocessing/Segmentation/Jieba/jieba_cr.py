import os
import jieba

names=os.listdir('criteria')

count = 0
if(not os.path.exists('semi-labeled-data')):
    os.mkdir('semi-labeled-data')

print(len(names))
for name in names:
    path=os.path.join('criteria', name)
    with open(path, 'r', encoding = 'utf-8') as f:
        text = f.read()
    lists = ['<', '>', '≤', '≥']
    if('<' in text or '>' in text, '≤' in text or '≥' in text):
        text=text.strip()
        seg_list=jieba.cut(text, cut_all=False)
        flag = 0
        string = ""
        for item in seg_list:
            if(item == ' '):
                continue
            if(item in lists):
                flag = 3
            if(flag>0 and item not in [' ', '\n', '\t', '.', ',', ';', '//']):
                flag -= 1
                string += "{}\t{}\n".format(item, 'NUMBER')
            else:
                if(item in ['\r', '\n', '\t']):
                    string += "{}\t{}\n".format('.', 'ELSE')
                else:
                    string += "{}\t{}\n".format(item, 'ELSE')
        with open('semi-labeled-data/{}.txt'.format(count), 'w+', encoding = 'utf-8') as g:
            g.write(string.strip())
            count += 1
print(count)
