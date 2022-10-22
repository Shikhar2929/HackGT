# IMPORTING DEPENDENCIES
import time
import json
from urllib import request
from bs4 import BeautifulSoup


BASE = 'https://www.bing.com'
URL = 'https://www.bing.com/search?q={}+media+entertainment+industry'
headers = {'User-Agent': ''}
start = time.time()


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
for service in service_data[start_point:]:
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
