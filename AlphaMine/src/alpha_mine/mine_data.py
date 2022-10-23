from abstractions import *


def collect_data():
    classes_file = input('Enter classes file: ')
    with open(classes_file) as file:
        classes = file.read().strip().split('\n')
    setup(classes)
    dtype = input('Enter data type (text/image): ')
    if dtype == 'text':
        num_pages = int(input('Enter number (0-66 inclusive) of pages per class: '))
        if num_pages not in range(0, 67):
            raise ValueError('Bad input. Number must be in range [0, 66].')
        mine(classes, dtype, num_samples=num_pages)
    elif dtype == 'image':
        num_images = int(input('Enter number (0-500 inclusive) of images per class: '))
        if num_images not in range(0, 501):
            raise ValueError('Bad input. Number must be in range [0, 500].')
        resize = input('Do you want to resize image? (y/n): ')
        if resize != 'y' and resize != 'n':
            raise ValueError('Bad input. Enter y/n to resize image.')
        elif resize == 'y':
            width = int(input('Enter image width (0-1920 inclusive) in pixels: '))
            if width not in range(0, 1921):
                raise ValueError('Bad input. Width must be in range [0, 1920].')
            height = int(input('Enter image height (0-1920 inclusive) in pixels: '))
            if height not in range(0, 1921):
                raise ValueError('Bad input. Height must be in range [0, 1920].')
        grayscale = input('Do you want to grayscale images? (y/n): ')
        if grayscale != 'y' and grayscale != 'n':
            raise ValueError('Bad input. Enter y/n for grayscale.')
        boundary_box = input('Do you want to draw boundary boxes around image objects? (y/n): ')
        if boundary_box != 'y' and boundary_box != 'n':
            raise ValueError('Bad input. Enter y/n for boundary box.')
        if resize == 'y':
            mine(classes, dtype, num_samples=num_images, size=(width, height), grayscale=grayscale=='y', boundary_box=boundary_box=='y')
        else:
            mine(classes, dtype, num_samples=num_images, grayscale=grayscale=='y', boundary_box=boundary_box=='y')
    else:
        raise ValueError('Bad input. Enter text/image.')


if __name__ == '__main__':
    collect_data()
    # parse_file_structure()
    print('process complete')
