# IMPORTING DEPENDENCIES
import time
import os
import json
from urllib import request
import requests
from bs4 import BeautifulSoup


# VARIABLE DEFINITIONS
encoder = json.JSONEncoder()
BASE = 'https://www.bing.com'
URL = 'https://www.bing.com/images/search?q={}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
start = time.time()
summary = {}


# MAIN FUNCTION
def image_query(classes):
    dir = os.path.join('./', "Data")
    os.mkdir(dir)
    for query in classes:
        summary[query] = []
        classDir= os.path.join('./Data/', query)
        os.mkdir(classDir)
        req = request.Request(url=URL.format(query.replace('_', '+')), headers=headers)
        try:
            resp = request.urlopen(req)
        except:
            break
        else:
            try:
                soup = BeautifulSoup(resp.read(), 'html.parser')
            except:
                break
            resp.close()
            for tag in soup(['style', 'script']):
                tag.decompose()
            images = soup.find_all("a", {"class": "iusc"})
            counter = 0
            for image in images:
                d = {}
                print(image['href'])
                d['link'] = image['href']
                image_data = requests.get(BASE + image['href']).content
                with open('./Data/' + query, 'w') as handler:
                    handler.write(image_data)
                counter += 1
                summary[query].append(d)

    # JSON SUMMARY
    try:
        open('data/img_summary.json', 'x')
    except:
        pass
    with open('data/img_summary.json', 'w') as file:
        file.write(encoder.encode(summary))


image_query(["Smith"])
