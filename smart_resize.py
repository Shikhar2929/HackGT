from PIL import Image
def smart_resize(image, size):
    width, height = image.size
    black = (0, 0, 0)
    result = Image.new(image.mode, (max(width, height), max(width, height)), black)
    result.paste(image, (0, 0))
    result = result.resize(size)
    return result

    
