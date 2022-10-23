import os
from PIL import Image


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
    pass


image = Image.open('img.png')
smart_resize(image, (800, 800))
