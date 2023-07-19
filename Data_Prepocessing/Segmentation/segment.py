#!/usr/bin/env python
# coding: utf-8

import os

RawPath='/Users/dogtail/Documents/biotech/AI/raw'
OutPath='/Users/dogtail/Documents/biotech/AI/segment'

def write_to_file(file, content):
    with open(os.path.join(OutPath, file), 'w+', encoding='utf-8') as f:
        f.write(content)

def label_file(file):
    file_path = os.path.join(RawPath, file)
    fp = open(file_path, 'r')
    data = fp.read()
    data = data.replace('\s', '')
    sentence = ""
    seg_output = ""
    for element in data:
        if element.__contains__('，'):
            sentence += '\n\n'
            seg_output += sentence
            sentence = ""
        elif element.__contains__('。'):
            sentence += '\n\n'
            seg_output += sentence
            sentence = ""
        elif element.__contains__('？'):
            sentence += '\n\n'
            seg_output += sentence
            sentence = ""
        else:
            sentence += element
    write_to_file(file, seg_output)

files = os.listdir(RawPath)
for file in files:
    label_file(file)
