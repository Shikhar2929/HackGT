# IMPORTING DEPENDENCIES
from abstractions import setup
import time
import json
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PIL import Image

chrome_options = Options()
chrome_options.add_argument("--headless")

# VARIABLE DEFINITIONS
encoder = json.JSONEncoder()
BASE = 'https://www.bing.com'
URL = 'https://www.bing.com/images/search?q={}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
start = time.time()
summary = {}


# MAIN FUNCTION
def image_query(classes, size):
    setup(classes)
    for query in classes:
        req = request.Request(url=URL.format(query.replace('_', '+')), headers=headers)
        try:
            resp = request.urlopen(req)
        except:
            break
        else:
            try:
                soup = BeautifulSoup(resp.read(), 'html.parser')
            except:
                pass
            resp.close()
            for tag in soup(['style', 'script']):
                tag.decompose()
            images_data = soup.find_all("a", {"class": "iusc"})
            counter = 0;
            for image_link in images_data:
                href = image_link['href']
                image_req = request.Request(url=BASE + href, headers=headers)
                image_resp = request.urlopen(image_req)
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                driver.get(BASE + href)
                time.sleep(1)
                image_site = driver.page_source
                image_soup = BeautifulSoup(image_site, "html.parser")
                driver.quit()
                for tag in image_soup(['style', 'script']):
                    tag.decompose()
                image_resp.close()
                image = image_soup.find("div", {"id": "mainImageWindow"})
                image = image['data-m'][1:-1].split(",")
                murl = image[2]
                murl = murl[8:-1]
                ext = murl[murl.rfind(".")+1:]
                image_req = request.Request(murl, headers=headers)
                try:
                    image_resp = request.urlopen(image_req)
                except:
                    pass
                else:
                    path = './data/{}/{}.{}'.format(query, "img" + str(counter), ext)
                    try:
                        open(path, 'x')
                    except:
                        print("\n\n\n\n Failed")
                    else:
                        with open(path, 'wb') as file:
                            file.write(image_resp.read())
                            image_resp.close()
                            im = Image.open(path)
                            im = im.resize(size)
                            im.save(path)
                        counter += 1
            

image_query(["Lebron_James"], (720, 720))
        


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


image_query(["Smith"])
'''
