#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 17:09:13 2023

@author: yingli
"""
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

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
#from selenium.common.exceptions import NoSuchElementException

class SearchModel:
    @classmethod
    def search_TA98(cls):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("detach", True)
        page = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
        page.get('https://taviewer.openanatomy.org/?lang=en')
        sleep(20)
        tree = page.find_element(By.CLASS_NAME, 'taviewer-tree').find_element(By.TAG_NAME, 'ul')
        while True:
            try:
                switcher = tree.find_element(By.CLASS_NAME, 'ant-tree-switcher_close')
                switcher.find_element(By.TAG_NAME, 'i').click()
                sleep(26)
            except:
                continue
        with open('TA98.hqt', 'w+', encoding='utf-8') as f:
            for value in tree.find_elements(By.CLASS_NAME, 'ant-tree-title'):
                f.write(value.text)
 
SearchModel.search_TA98()               
                
                