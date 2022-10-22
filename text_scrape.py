# todo
# Text code cleanup
# Parameters
# Multi-pages
# JSON summary


# IMPORTING DEPENDENCIES
import os
import time
from json import JSONEncoder
from urllib import request
from bs4 import BeautifulSoup


# VARIABLE DEFINITIONS
BASE = 'https://www.bing.com'
URL = 'https://www.bing.com/search?q={}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
start = time.time()
num_results = 0
summary = {}
encoder = JSONEncoder()
max_pages = int(input('Enter number of pages per class: '))

with open('classes.txt') as file:
    classes = file.read().split('\n')


def get_search_results(link):
    req = request.Request(url=link, headers=headers)
    try:
        resp = request.urlopen(req)
    except:
        return None
    else:
        try:
            soup = BeautifulSoup(resp.read(), 'html.parser')
        except:
            resp.close()
            return None
        else:
            resp.close()
            for tag in soup(['style', 'script']):
                tag.decompose()
            return soup


def get_page_text(link):
    try:
        req = request.Request(url=link, headers=headers)
    except:
        return ''
    else:
        try:
            resp = request.urlopen(req, timeout=5)
        except:
            return ''
        else:
            try:
                soup = BeautifulSoup(resp.read(), 'html.parser')
            except:
                resp.close()
                return ''
            else:
                resp.close()
                for tag in soup(['style', 'script']):
                    tag.decompose()
                return soup.get_text()


# SEARCH AND SCRAPE
for query in classes:
    text = ''
    links = []
    soup = get_search_results(URL.format(query))
    results = soup.find_all(name='li', attrs={'class': 'b_algo'})
    summary[query] = []

    if len(results) > max_pages:
        pages = soup.find_all(name='a', attrs={'class': 'b_widePag sb_bp'})
        for page in pages:
            soup = get_search_results(BASE + page['href'])
            results += soup.find_all(name='li', attrs={'class': 'b_algo'})
            if len(results) > max_pages:
                break

    for result in results:
        num_results += 1
        d = {}
        h = result.find_next(name='h2')
        d['title'] = h.get_text()
        links.append(h.find_next(name='a')['href'])
        d['link'] = links[-1]
        summary[query].append(d)

    for link in links:
        text += get_page_text(link)

    try:
        os.mkdir('data/{}'.format(query))
    except:
        pass
    try:
        open('data/{}/text.txt'.format(query), 'x')
    except:
        pass
    with open('data/{}/text.txt'.format(query), 'w') as file:
        file.write(text)

    print('class: {}\tresults collected: {}\ttime: {}s'.format(query, num_results, time.time() - start))


# JSON SUMMARY
try:
    open('data/text_summary.json', 'x')
except:
    pass
with open('data/text_summary.json', 'w') as file:
    file.write(encoder.encode(summary))
