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

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

chrome = Service(ChromeDriverManager(path=r'.\\webdriver').install())
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])


def get_names(ele, driver):
    """ parse elements with javascript, return name list
        ele: element in the list output from get_eles() 
        browser: the selenium auto-browser opened for parsing """
    # open pop-up window
    ele.click()
    pop_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="pop-mod pop_ks x-show"]')))
    # parse names
    time.sleep(1)
    key = pop_box.find_element(by=By.CSS_SELECTOR, value='div.tit.clear').text
    values = pop_box.find_element(by=By.CSS_SELECTOR, value='#datalist').text.split('\n')
    
    driver.execute_script("""
        $('.pop-mod').removeClass('x-show');
        enWinScroll();
    """)

    return {"subject": key, "experts": values}


def get_eles(string, url):
    """ request expertlist webpage, search keyword, e.g. 肿瘤, by regular expression, return elements contain javascript
        url: huaxi expertlist webpage
        string: disease keyword of interest 
        
        output as list of dict: 
        e.g. [{'subject': '头颈肿瘤科', 'experts': ['艾平', '陈念永', '邓窈窕', '邓锐', '段宝凤', '苟启桁', '官泳松', '贺萍', '贺庆', '何明敏', '姜愚', '蒋明', '李燕雏', '刘杰', '李梅', '刘磊', '罗勇', '任柯星']}, 
              {'subject': '腹部肿瘤科', 'experts': ['曹鹏', '陈虹悯', '曹丹', '陈烨', '成科', '代瑞红', '勾红峰', '郭文浩', '胡前程', '何建萍', '李志平', '廖正银', '罗德云', '李晓芬', '陆发承', '冷卫兵', '刘继彦', '李秋']}, 
              {'subject': '胸部肿瘤科', 'experts': ['宫友陵', '黄媚娟', '卢铀', '李艳莹', '刘咏梅', '纳飞飞', '彭枫', '王永生', '王瑾', '修位刚', '徐泳', '薛建新', '喻杨', '余敏', '邹炳文', '曾莎莎', '朱江', '周晓娟']}]"""
    # open the browser and request the page
    browser = webdriver.Chrome(service=chrome, options=option)
    while True:
        try:
            browser.get(url)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="tabsbox"]')))
        except TimeoutException:
            browser.refresh()
            continue
        else:
            eles = browser.find_elements(by=By.XPATH, value='//a[span[contains(text(), "{}")]]'.format(string))
            result_lst = []
            for ele in eles:
                names = get_names(ele, browser)
                result_lst.append(names)
            break
    browser.quit()

    return result_lst


if __name__ == '__main__':
    kword = "肿瘤"
    huaxi = 'http://www.wchscu.cn/expertlist.html'
    name_lst = get_eles(kword, huaxi)
    names = []
    for name_dict in name_lst:
        names.extend(name_dict['experts'])
    """ final output: name list write in txt file, one line one name """
    with open(r'.\output\expert.txt', 'w', encoding="utf-8") as out:
        for name in names:
            out.write(name + '\n')
    
        






