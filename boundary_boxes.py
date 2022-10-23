import cv2 as cv
import numpy as np
from json import JSONEncoder
import os
img = None
img0 = None
outputs = None
classes = open('coco.names').read().strip().split('\n')
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')
net = cv.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
ln = net.getLayerNames()
ln = [ln[i-1] for i in net.getUnconnectedOutLayers()]
def load_image(path, class_name, name):
    global img, img0, outputs, ln
    img0 = cv.imread(path)
    if img0 is None:
        return
    img = img0.copy()
    blob = cv.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(ln)
    outputs = np.vstack(outputs)
    create_dic(img, outputs, 0.9, name, class_name)
        
def create_dic(img, outputs, conf, file_name, current_class):
    my_dic = {file_name: []}
    if img is None:
        return
    H, W = img.shape[:2]
    for output in outputs:
        scores = output[5:]
        confidence = output[5]
        if confidence > conf:
            x, y, w, h = output[:4] * np.array([W, H, W, H])
            p0 = int(x - w//2), int(y - h//2)
            p1 = int(x + w//2), int(y + h//2)
            temp_dic = {'leftx': p0[0], 'lefty': p0[1], 'width': int(w), 'height': int(h), 'label': current_class}
            my_dic[file_name].append(temp_dic)
    encoder = JSONEncoder()
    print(my_dic)
    try:
        open("image_meta.json", "x")
    except: 
        pass
    with open("image_meta.json", "w") as file: 
        file.write(encoder.encode(my_dic))
def parse_file_structure():
    for root, dirs, files in os.walk('data'):
        for name in files:
            temp = os.path.join(root, name)
            list_root = str(root).split('\\')
            load_image(temp, list_root[-1], name)
parse_file_structure()