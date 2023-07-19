#!/usr/bin/env python
# coding: utf-8

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
