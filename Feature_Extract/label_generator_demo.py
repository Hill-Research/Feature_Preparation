#!/usr/bin/env python
# coding: utf-8

import os

RawPath='/Users/dogtail/Documents/biotech/AI/raw'
OutPath='/Users/dogtail/Documents/biotech/AI/label'

def write_to_file(file, content):
    with open(os.path.join(OutPath, file), 'w+', encoding='utf-8') as f:
        f.write(content)

def label_file(file):
    file_path = os.path.join(RawPath, file)
    fp = open(file_path, 'r')
    data = fp.read()
    data = data.replace('\s', '')
    label_output = ""
    for element in data:
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if element.__contains__('，'):
            label_output = label_output + element + ' [sep]\n'
        elif element.__contains__('。'):
            label_output = label_output + element + ' [sep]\n'
        elif element.__contains__('？'):
            label_output = label_output + element + ' [sep]\n'
        elif element in numbers:
            label_output = label_output + element + ' [number]\n'
        else:
            label_output = label_output + element + '\n'
    write_to_file(file, label_output)

files = os.listdir(RawPath)
for file in files:
    label_file(file)
