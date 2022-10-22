# todo
# Text code cleanup
# Parameters
# Multi-pages
# JSON summary


# IMPORTING DEPENDENCIES
import os
import time
from urllib import request
from bs4 import BeautifulSoup


# VARIABLE DEFINITIONS
BASE = 'https://www.bing.com'
URL = 'https://www.bing.com/search?q={}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
start = time.time()
num_results = 0

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

    # pages = soup.find_all(name='a', attrs={'class': 'b_widePag sb_bp'})
    # for page in pages:
    #     soup = get_search_results(BASE + page['href'])
    #     results += soup.find_all(name='li', attrs={'class': 'b_algo'})

    for result in results:
        num_results += 1
        links.append(result.find_next(name='h2').find_next(name='a')['href'])

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







    #
    # req = request.Request(url=URL.format(query), headers=headers)
    # try:
    #     resp = request.urlopen(req)
    # except:
    #     break
    # else:
    #     try:
    #         soup = BeautifulSoup(resp.read(), 'html.parser')
    #     except:
    #         break
    #     resp.close()
    #     for tag in soup(['style', 'script']):
    #         tag.decompose()
    #     results = soup.find_all(name='li', attrs={'class': 'b_algo'})
    #     pages = soup.find_all(name='a', attrs={'class': 'b_widePag sb_bp'})
    #     for page in pages:
    #         print(page['href'])


        #
        # for page in pages:
        #     req = request.Request(url=BASE + page['href'], headers=headers)
        #     try:
        #         resp = request.urlopen(req)
        #     except:
        #         break
        #     else:
        #         soup = BeautifulSoup(resp.read(), 'html.parser')
        #         resp.close()
        #         for tag in soup(['style', 'script']):
        #             tag.decompose()
        #         results = soup.findAll(name='div', attrs={'class': 'b_caption'})
        #         text = []
        #         for result in results:
        #             x = result.findAll(name='p')
        #             if len(x) > 0:
        #                 text.append(''.join(x[0].strings))
        # print(results)

'''    inv_chars = []
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
'''


# Text Search Link: https://www.bing.com/search?q=cat&FORM=HDRSC1
# Image Search Link: https://www.bing.com/images/search?q=cat&form=HDRSC2&first=1&tsc=ImageHoverTitle
