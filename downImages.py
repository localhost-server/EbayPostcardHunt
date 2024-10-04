import os
import concurrent.futures as cf
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup as bs4
import requests
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import shutil
import time

# reading the links removing \n from links from last
with open('searched_links.txt', 'r') as file:
    searched_links = file.readlines()

links=set()
for i in searched_links:
    if "http" in i:
        links.add(i[:-1])
searched_links=links


# removing all saved htmls
htmls= os.listdir('htmls')
def remh(i):
    os.remove(f'htmls/{i}')

with ThreadPoolExecutor(max_workers=50) as pool:
    pool.map(remh, htmls)

# removing all saved images
imgs= os.listdir('down_imgs')
def remi(i):
    os.remove(f'down_imgs/{i}')

with ThreadPoolExecutor(max_workers=50) as pool:
    pool.map(remi, imgs)

# for image in os.listdir('down_imgs'):
#     os.remove(f'down_imgs/{image}')

if not os.path.exists('down_imgs'):
    os.mkdir('down_imgs')

if not os.path.exists('htmls'):
    os.mkdir('htmls')

# saving the html and images
def saveHtmlImg(i):
    fname=i.split('?')[0].split('/')[-1]
    if os.path.exists(f"htmls/{fname}.html") and os.path.exists(f"down_imgs/{fname}.jpg"):
        # print(f"Already saved {fname}")
        return False
    req=requests.get(i)
    # print(req)
    if req.status_code==200:
        # saving the page
        try:
            # print(fname)
            with open(f"htmls/{fname}.html", 'w',encoding='utf-8') as file:
                file.write(req.text)
            # print(f"Saved {fname}")
        except Exception as e:
            print(f"Error in saving html {i} \n{e}")

        if os.path.exists(f"down_imgs/{fname}.jpg"):
            # print(f"Already saved {fname}.jpg")
            pass
        else:
            # with open(f'htmls/{fname}.html', 'r', encoding='utf-8') as file:
            #     htmreq = file.read()
            soup = bs4(req.text, 'html.parser')
            # div.ux-image-carousel-item.image-treatment.active.image
            element = soup.find_all('div', {'class': 'ux-image-carousel-item image-treatment active image'})
            try:
                SrcOfImage = element[1].find('img')['src']
            except Exception as e:
                SrcOfImage = element[1].find('img')['data-src']
            
             # downloading the image
            try:
                req = requests.get(SrcOfImage)
                if req.status_code == 200:
                    image=Image.open(BytesIO(req.content))
                    if image.mode == 'WEBP' or image.mode == 'RGBA':
                        image = image.convert('RGB')
                    re_image=image.resize((640,640))
                    re_image.save(f"down_imgs/{fname}.jpg",'JPEG')
                    # print(f"Saved {fname}.jpg")
            
            except Exception as e:
                print(f"Error in downloading image {i} \n {e}")
                
        return True
    else:
        return False


if __name__=="__main__":
    import time
    start = time.time()
    # running thread pool executor

    with ProcessPoolExecutor(max_workers=50) as pool:
        pool.map(saveHtmlImg, searched_links)
    # with cf.ThreadPoolExecutor(max_workers=150) as executor:
    #     executor.map(saveHtmlImg, searched_links)

    print(f"Time taken: {time.time()-start}")   