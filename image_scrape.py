# IMPORTING DEPENDENCIES
from abstractions import setup
import time
import os
import json
from urllib import request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager


# VARIABLE DEFINITIONS
encoder = json.JSONEncoder()
BASE = 'https://www.bing.com'
URL = 'https://www.bing.com/images/search?q={}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
start = time.time()
summary = {}
driver = webdriver.Chrome()


def image_query(classes):
    for query in classes:
        driver.get(URL.format(query))



# # MAIN FUNCTION
# def image_query(classes):
#     dir = os.path.join('./', "Data");
#     os.mkdir(dir);
#     for query in classes:
#         classDir= os.path.join('./Data/', query)
#         os.mkdir(classDir)
#         req = request.Request(url=URL.format(query.replace('_', '+')), headers=headers)
#         try:
#             resp = request.urlopen(req)
#         except:
#             break
#         else:
#             try:
#                 soup = BeautifulSoup(resp.read(), 'html.parser')
#             except:
#                 break
#             resp.close()
#             for tag in soup(['style', 'script']):
#                 tag.decompose()
#             images_data = soup.find_all("a", {"class": "iusc"})
#             counter = 0;
#             for image_link in images_data:
#                 href = image_link['href']
#                 image_req = request.Request(url=BASE + href, headers=headers)
#                 image_resp = request.urlopen(image_req)
#                 driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#                 driver.get(BASE + href)
#                 time.sleep(1)
#                 image_site = driver.page_source
#                 soup = BeautifulSoup(image_site, "html.parser")
#                 driver.quit()
#                 image_soup = BeautifulSoup(image_resp.read(), 'html.parser')
#                 for tag in image_soup(['style', 'script']):
#                     tag.decompose()
#                 image_resp.close()
#                 print(image_soup)
#                 file_ext = image_soup.find("div", {"id": "detailWindow"})
#                 print(file_ext)
#                 break
'''
                try:
                    open('data/{}/'.format(query), 'x')
                except:
                    pass
                with open('data/text_summary.json', 'w') as file:
                    file.write(encoder.encode(summary))
'''



image_query(["Lebron_James"])
