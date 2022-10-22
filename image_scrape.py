# IMPORTING DEPENDENCIES
import time
import os
import json
from urllib import request
import requests
from bs4 import BeautifulSoup


# VARIABLE DEFINITIONS
decoder = json.JSONDecoder()
encoder = json.JSONEncoder()
BASE = 'https://www.bing.com'
URL = 'https://www.bing.com/images/search?q={}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
start = time.time()


# MAIN FUNCTION
def image_query(classes):
    dir = os.path.join('./', "Data");
    os.mkdir(dir);
    for query in classes:
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
            counter = 0;
            for image in images:
                print(image['href'])
                image_data = requests.get(BASE + image['href']).content
                with open('./Data/' + query, 'w') as handler:
                    handler.write(image_data)
            


image_query(["Smith"])
        


'''
# DATA READING
with open('../data/bing_io.json') as file:
    text_corpus = file.read()
if len(text_corpus) != 0:
    text_corpus = decoder.decode(text_corpus)
    start_point = max([data[0] for data in text_corpus]) - 1
else:
    text_corpus = []
    start_point = 0


with open('../data/services.json') as file:
    service_data = decoder.decode(file.read())


# SEARCH AND SCRAPE
def text_query():
    for service in service_data[start_point:]:
        # pruning non ASCIIs
        inv_chars = []
        for char in service['Service Name']:
            if ord(char) not in range(128):
                inv_chars.append(char)
        for char in inv_chars:
            service['Service Name'] = service['Service Name'].replace(char, '').lower()
        req = request.Request(url=URL.format(service['Service Name'].replace(' ', '+')), headers=headers)
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
            results = soup.findAll(name='div', attrs={'class': 'b_caption'})
            text = []
            for result in results:
                x = result.findAll(name='p')
                if len(x) > 0:
                    text.append(''.join(x[0].strings))
            pages = soup.findAll(name='a', attrs={'class': 'b_widePag sb_bp'})
            for page in pages:
                req = request.Request(url=BASE + page['href'], headers=headers)
                try:
                    resp = request.urlopen(req)
                except:
                    break
                else:
                    soup = BeautifulSoup(resp.read(), 'html.parser')
                    resp.close()
                    for tag in soup(['style', 'script']):
                        tag.decompose()
                    results = soup.findAll(name='div', attrs={'class': 'b_caption'})
                    text = []
                    for result in results:
                        x = result.findAll(name='p')
                        if len(x) > 0:
                            text.append(''.join(x[0].strings))
            text_corpus += [[service['Service Name'], t] for t in text]
            print('results collected: {}\ttime: {}s\tpages scanned: {}\tservice: {}'.format(len(text_corpus), time.time() - start, len(pages) + 1, service['vtr_id']))
            # time.sleep(10)


# SAVING
with open('../data/bing_io.json', 'w') as file:
    file.write(encoder.encode(text_corpus))
    file.close()



# Text Search Link: https://www.bing.com/search?q=cat&FORM=HDRSC1
# Image Search Link: https://www.bing.com/images/search?q=cat&form=HDRSC2&first=1&tsc=ImageHoverTitle
'''