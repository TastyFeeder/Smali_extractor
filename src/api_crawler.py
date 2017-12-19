# TODO : crawler all api from https://developer.android.com/reference/packages.html
#        every li under "dac-reference-nav-list" is a package 
#        traval all package and crawler every class

import scrapy
import requests
from bs4 import BeautifulSoup

'''
class api_spider(scrapy.Spider):
    name = "api_spider"
    start_url = ['https://developer.android.com/reference/packages.html']
    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            pass
'''

def package_crawler():
    url = 'https://developer.android.com/reference/packages.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    the_div = soup.find_all('div', 'dac-reference-nav')
    the_ul = the_div[0].find_all('ul')
    the_li = the_ul[0].find_all('li')
#    print(the_li)
    for li in the_li:
        package_name = li.getText().strip()
        link = li.find('a').get('href')
        print(package_name, " ===> ", link)
        
def class_crawler(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    the_table = soup.find_all('table', 'jd-sumtable-expando')
    
    pass
#    print(the_ul)

if __name__ == "__main__":
    class_crawler('https://developer.android.com/reference/android/package-summary.html')
#    package_crawler()
