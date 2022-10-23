from abstractions import *


def collect_data():
    classes_file = input('Enter classes file: ')
    with open(classes_file) as file:
        classes = file.read().strip().split('\n')
    setup(classes)
    dtype = input('Enter data type (text/image): ')
    if dtype == 'text':
        num_pages = int(input('Enter number of pages per class: '))
        mine(classes, dtype, num_samples=num_pages)
    elif dtype == 'image':
        num_images = int(input('Enter number of images per class: '))
        width = int(input('Enter image width (in pixels): '))
        height = int(input('Enter image height (in pixels): '))
        grayscale = input('Do you want to grayscale images? (y/n): ')
        boundary_boxes = input('Do you want to draw boundary boxes around image objects? (y/n): ')
    else:
        raise ValueError("Bad input. Enter text/image.")
