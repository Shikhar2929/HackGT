# IMPORTING DEPENDENCIES
import os
import time
import cv2 as cv
import numpy as np
from pprint import pprint
from json import JSONEncoder
from urllib import request
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# VARIABLE DEFINITIONS
BASE = 'https://www.bing.com'
URL = 'https://www.bing.com/search?q={}'
IMG_URL = 'https://www.bing.com/images/search?q={}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15")
img = None
img0 = None
outputs = None
classes = open('../../static/coco.names').read().strip().split('\n')
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')
net = cv.dnn.readNetFromDarknet('../../static/yolov3.cfg', '../../static/yolov3.weights')
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]


def load_image(path, class_name, name):
    global img, img0, outputs, ln
    img0 = cv.imread(path)
    if img0 is None:
        return
    img = img0.copy()
    blob = cv.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(ln)
    outputs = np.vstack(outputs)
    return create_dic(img, outputs, 0.8, name, class_name)


def create_dic(img, outputs, conf, file_name, current_class):
    name = current_class + '/' + file_name
    my_dic = {name: []}
    if img is None:
        return my_dic
    H, W = img.shape[:2]
    for output in outputs:
        confidence = output[5]
        if confidence > conf:
            x, y, w, h = output[:4] * np.array([W, H, W, H])
            p0 = int(x - w // 2), int(y - h // 2)
            temp_dic = {'leftx': p0[0], 'lefty': p0[1], 'width': int(w), 'height': int(h), 'label': current_class}
            my_dic[name].append(temp_dic)
    return my_dic


def parse_file_structure():
    data = []
    for root, dirs, files in os.walk('data'):
        for name in files:
            print(root)
            temp = os.path.join(root, name)
            list_root = str(root).split('\\')
            data.append(load_image(temp, list_root[-1], name))
    encoder = JSONEncoder()
    try:
        open('data/image_meta.json', 'x')
    except:
        pass
    with open('data/image_meta.json', 'w') as file:
        file.write(encoder.encode(data))
    pprint(data)



def setup(classes):
    try:
        os.mkdir('data')
    except:
        pass
    for c in classes:
        try:
            os.mkdir('data/{}'.format(c))
        except:
            pass


def smart_resize(image, size):
    width, height = image.size
    black = (0, 0, 0)
    result = Image.new(image.mode, (max(width, height), max(width, height)), black)
    result.paste(image, (0, 0))
    result = result.resize(size)
    return result


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


def mine_text(classes, num_pages):
    setup(classes)
    start = time.time()
    num_results = 0
    summary = {}
    encoder = JSONEncoder()

    # SEARCH AND SCRAPE
    for query in classes:
        text = ''
        links = []
        soup = get_search_results(URL.format(query))
        results = soup.find_all(name='li', attrs={'class': 'b_algo'})
        summary[query] = []

        if len(results) > num_pages:
            pages = soup.find_all(name='a', attrs={'class': 'b_widePag sb_bp'})
            for page in pages:
                soup = get_search_results(BASE + page['href'])
                results += soup.find_all(name='li', attrs={'class': 'b_algo'})
                if len(results) > num_pages:
                    break

        if len(results) > num_pages:
            results = results[:num_pages]

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


def mine_image(classes, numExamples, size, performGrayscale):
    setup(classes)
    summary = {}
    encoder = JSONEncoder()
    start = time.time()
    for query in classes:
        summary[query] = []
        toDel = []
        req = request.Request(url=IMG_URL.format(query.replace('_', '+')), headers=headers)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        try:
            driver.get(IMG_URL.format(query.replace('_', '+')))
            time.sleep(0.5)
            scrolls = 0
            while (scrolls < numExamples / 15):
                driver.execute_script("window.scrollBy(0,document.body.scrollHeight);", "")
                time.sleep(1)
                try:
                    see_more_xpath = '//*[@id="bop_container"]/div[2]/a'
                    see_more_button = driver.find_element(By.XPATH, see_more_xpath)
                    driver.execute_script('arguments[0].scrollIntoView(true);', see_more_button)
                    driver.execute_script('window.scrollBy(0, -100);', '')
                    time.sleep(1)
                    see_more_button.click()
                    time.sleep(3)
                except:
                    pass
                else:
                    while (scrolls < numExamples / 15):
                        driver.execute_script("window.scrollBy(0,document.body.scrollHeight);", "")
                        driver.execute_script('window.scrollBy(0, -300);', '')
                        time.sleep(1)
                        scrolls += 1;
                    break
                scrolls += 1
            resp = driver.page_source;
        except:
            pass
        else:
            try:
                soup = BeautifulSoup(resp, 'html.parser')
                driver.quit()
            except:
                pass
            for tag in soup(['style', 'script']):
                tag.decompose()
            images_data = soup.find_all("a", {"class": "iusc"})

            counter = 0;
            images_stored = 0;
            # goes through class samples
            while (images_stored < numExamples):
                image_link = images_data[counter]
                href = image_link['href']
                image_req = request.Request(url=BASE + href, headers=headers)
                image_resp = request.urlopen(image_req)
                # loads webpage with image
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                try:
                    driver.get(BASE + href)
                    time.sleep(0.5)
                    image_site = driver.page_source
                except:
                    pass
                else:
                    try:
                        image_soup = BeautifulSoup(image_site, "html.parser")
                        driver.quit()
                    except:
                        pass
                    else:
                        for tag in image_soup(['style', 'script']):
                            tag.decompose()
                        image_resp.close()
                        # finds image info (e.g. link, etc)
                        image = image_soup.find("div", {"id": "mainImageWindow"})
                        image = image['data-m'][1:-1].split(",")
                        # gets image link
                        murl = image[2]
                        murl = murl[8:-1]
                        # gets file extension
                        ext = murl[murl.rfind(".") + 1:]
                        if (ext.find("?") != -1):
                            ext = ext[:ext.find("?")]
                        if (ext not in ["jpg", "jpeg", "png", "gif"]):
                            if (murl.find("jpg") != -1):
                                ext = "jpg"
                            elif (murl.find("jpeg") != -1):
                                ext = "jpeg"
                            elif (murl.find("png") != -1):
                                ext = "png"
                            elif (murl.find("gif") != -1):
                                ext = "gif"
                            else:
                                counter += 1
                                print("Image could not be processed.")
                                continue
                        image_req = request.Request(murl, headers=headers)
                        # writes image to file
                        try:
                            image_resp = request.urlopen(image_req)
                        except:
                            pass
                        else:
                            path = './data/{}/{}.{}'.format(query, "img" + str(counter), ext)
                            try:
                                open(path, 'x')
                            except:
                                print("File could not be created.")
                                pass
                            with open(path, 'wb') as file:
                                file.write(image_resp.read())
                                image_resp.close()
                                error = False
                                try:
                                    im = Image.open(path)
                                    if (size != None):
                                        im = smart_resize(im, size)
                                    if (performGrayscale):
                                        im = im.convert('L')
                                    im.save(path)
                                except:
                                    toDel.append(path)
                                else:
                                    images_stored += 1
                                    summary[query].append({'path': path, 'link': murl})
                counter += 1
        for rm in toDel:
            os.remove(rm)
        print('class: {}\tresults collected: {}\ttime: {}s'.format(query, images_stored, time.time() - start))
    # JSON SUMMARY
    try:
        open('data/image_summary.json', 'x')
    except:
        pass
    with open('data/image_summary.json', 'w') as file:
        file.write(encoder.encode(summary))


def mine(classes, dtype, num_samples=100, size=None, grayscale=False, boundary_box=False):
    setup(classes)
    if dtype == 'text':
        mine_text(classes, num_samples)
    else:
        mine_image(classes, num_samples, size, grayscale)
        if boundary_box:
            parse_file_structure()
