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

import requests
from bs4 import BeautifulSoup, Comment
from urllib.parse import urlparse, urlunparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

driver = webdriver.Chrome()
driver.maximize_window()
url = 'https://www.clinicaltrials.gov/ct2/show/'
main_url = 'https://www.clinicaltrials.gov/ct2/results?cond=&term=&type=Intr&rslt=&age_v=&gndr=&intr=Drug&titles=&outc=&spons=&lead=&id=&cntry=&state=&city=&dist=&locn=&rsub=&strd_s=&strd_e=&prcd_s=&prcd_e=&sfpd_s=&sfpd_e=&rfpd_s=&rfpd_e=&lupd_s=&lupd_e=&sort='
driver.get(main_url)
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@name='theDataTable_length']/option[@value='100']")))
    element.click()
    time.sleep(2)
    for i in range(11):
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@id="theDataTable_next"]')))
            element.click()
            time.sleep(2)
        except TimeoutException:
            driver.refresh()
            continue
except TimeoutException:
    driver.refresh()

content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content, 'html.parser')

# find the hrefs and page number
links = []
hrefs = []
titles = []
data_table = soup.find('table', {'id':'theDataTable'})
tds = data_table.find_all('td')
for table in tds:
    links += table.find_all('a')
for link in links:
    if ( ((link.get('id')) is None) and 
        (link.get('title').startswith('Show study NCT')) ):
        hrefs.append(link.get('href'))
        titles.append(link.text)

# Find eligibility criteria
for i in range(len(hrefs)):
    new_url = urljoin(url, hrefs[i])
    sub = requests.get(new_url)
    sub_soup = BeautifulSoup(sub.content, 'html.parser')
    
    for comment in sub_soup.findAll(string=lambda string:isinstance(string, Comment)):
        if comment in [' eligibility_section ']:
            content = comment.find_next()
            cr = content.find('div', {'class': 'ct-header3'})
            if (cr.text.startswith('Crit')):
                include = cr.find_next()
                include_cr = include.text.split('Exclusion', 1)[0]
                break
            else:
                incr = cr.find_next('p', string = 'Inclusion Criteria:')
                if (incr.find_next().name == 'ul'):
                        include = incr.find_next()
                        include_cr = incr.text.split('Exclusion', 1)[0]
                        break
                else:
                        include = incr.find_next('ol')
                        include_cr = include.text.split('Exclusion', 1)[0]
                        break

    filename = str(hrefs[i])[10:21] + '.txt'
    with open(filename, 'w+') as f:
        f.write("%s \n%s" % (titles[i], 'Eligibility Criteria'))
        f.write(include_cr)
        print(filename,"wrote")
        f.close() 
