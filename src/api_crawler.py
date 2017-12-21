# TODO : crawler all api from https://developer.android.com/reference/packages.html
#        every li under "dac-reference-nav-list" is a package 
#        traval all package and crawler every class

import requests
import pickle
from utils import write_plk
from bs4 import BeautifulSoup
from itertools import takewhile, chain
import html

PATH = "test.plk"

def package_crawler():
    url = 'https://developer.android.com/reference/packages.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    the_div = soup.find_all('div', 'dac-reference-nav')
    the_ul = the_div[0].find_all('ul')
    the_li = the_ul[0].find_all('li')
#    print(the_li)
    api_dict = {}
    for li in the_li[2:]:
        package_name = li.getText().strip()
        link = li.find('a').get('href')
        print( "============> ",package_name, link)
        api_dict.update({package_name : [] })
#        print("\t||")
        class_crawler(link, api_dict[package_name])
    path = write_plk(PATH, api_dict)
    print(api_dict)
    print("save api dict to {}".format(path))

def class_crawler(url, class_list):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    h2tag = soup.find_all('h2')
    x = 0
    for i in h2tag:
        if i.getText().strip() == "Classes":
            x= h2tag.index(i)
    the_table = h2tag[x].find_next('table')
    trs = the_table.find_all('tr')
#    print(trs)
    for tr in trs:
#        print(tr)
        class_name = tr.getText().strip().split(' ')[0]
        class_name =  class_name.replace("\n","")
        class_name =  class_name.replace(html.unescape('&nbsp')," ")
        print("\t====>",repr(class_name))
        class_list.append(class_name)
#    print(the_ul)




if __name__ == "__main__":
#    class_crawler('https://developer.android.com/reference/com/android/internal/util/package-summary.html')
    package_crawler()
