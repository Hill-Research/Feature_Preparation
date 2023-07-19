#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 17:09:13 2023

@author: yingli
"""
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
                
                