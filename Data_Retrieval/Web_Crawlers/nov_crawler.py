

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urljoin

main_url = 'https://www.recruiting-trials.novartis.com/recruiting-clinical-trials?page='
url = 'https://www.recruiting-trials.novartis.com/'
for i in range(1):
    # Fetch the  page
    page_url = main_url + str(i)
    page = requests.get(page_url)
    # Parse the page
    soup = BeautifulSoup(page.content, 'html.parser')
    # Find the hrefs
    links=[]
    hrefs=[]
    tables = soup.find_all('td', {'class': 'views-field views-field-title'})
    for table in tables:
        links += table.find_all('a')
    hrefs = [link['href'] for link in links]
    # loop all links
    for link in hrefs:
        new_url = urljoin(url, link)
        sub_page = requests.get(new_url)
        #print("URL:", new_url)
        sub_soup = BeautifulSoup(sub_page.content, 'html.parser')
        # Find trial title
        title = sub_soup.find('h1', {'id': "page-title"})
        # Find the criterias
        cr = sub_soup.find('div',{'class' : 'field field-name-field-nct-eligibility-criteria field-type-text-long field-label-hidden'})
        filename = str(link)[-11:] + '.txt'
        # Write to a .txt file
        with open(filename, 'w+') as f:
            f.write("%s \n%s\n%s" % (title.text, "Eligibility Criteria:", cr.text))
            print(filename,"wrote")
            f.close()
