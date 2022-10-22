import requests
from bs4 import BeautifulSoup
import os

if __name__ == "__main__":
    def imagedown(url, folder):
       if not os.path.isdir(folder): #cleaner to use os.path.isdir when checking for folder existence
          os.mkdir(folder)
       soup = BeautifulSoup(requests.get(url).text, 'html.parser')
       for i, a in enumerate(soup.select('img:is(.mainman, .thumbbot)'), 1):
            count = 1
            name = soup.select_one('div.head2BR').text+f'({i})'
            with open(os.path.join(folder, str(count) + '.jpg'), 'wb') as f: #join folder name to new image name
               im = requests.get(a['src'])
               f.write(im.content)
            count += 1

imagedown('https://www.whiteline.com.au/product_detail4.php?part_number=KBR15', 'whiteline_images')
imagedown('https://www.whiteline.com.au/product_detail4.php?part_number=W13374', 'whiteline_images')
imagedown('https://www.whiteline.com.au/product_detail4.php?part_number=BMR98', 'whiteline_images')
imagedown('https://www.whiteline.com.au/product_detail4.php?part_number=W51210', 'whiteline_images')
imagedown('https://www.whiteline.com.au/product_detail4.php?part_number=W51211', 'whiteline_images')