import time
import os
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup as bs
import requests
import matplotlib.pyplot as plt
import random
import shutil
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pymongo
from imagededup.methods import CNN
from imagededup.utils import CustomModel
from imagededup.utils.models import MobilenetV3
from playwright.async_api import async_playwright
import os

cookieFol=os.listdir("cookies")
cookiefile=random.choice(cookieFol)
with open(f'cookies/{cookiefile}', 'r') as file:
    cookies = json.load(file)

# Load cookies from the text file
# with open('Authcookies.txt', 'r') as file:
#     cookies = json.load(file)

# Defining Functions
async def open_browser(page):
    # page.set_viewport_size({'width': 1900, 'height': 1000})
    await page.emulate_media(color_scheme='dark')
    weblink = "https://www.ebay.com/sh/research?marketplace=EBAY-US&tabName=SOLD"
    await page.goto(weblink)
    await page.wait_for_timeout(2000)
    return page

async def runResearching(cookies):
    async with async_playwright() as p:
        # Ensure all cookies have valid 'sameSite' values
        valid_same_site_values = {"Strict", "Lax", "None"}
        for cookie in cookies:
            # Fix 'sameSite' if invalid or unspecified
            if cookie.get("sameSite") not in valid_same_site_values:
                cookie["sameSite"] = "Lax"  # Default to "Lax" or choose another valid value

            # Ensure 'sameSite' is not None (could lead to another error)
            if cookie.get("sameSite") is None:
                cookie["sameSite"] = "Lax"

        args = ["--disable-blink-features=AutomationControlled"]
        # username = os.getenv("OxylabUser")
        # passwd = os.getenv("OxylabPass")
        # num=random.randint(1,21)
        # if num<10:
        #     proxy = f'isp.oxylabs.io:800{num}'
        # else:
        #     proxy = f'isp.oxylabs.io:80{num}'
        # proxy="brd.superproxy.io:22225"
        browser = await p.chromium.launch_persistent_context('',args=args, headless=False)
                # ,proxy={
                # "server": proxy,
                # "username": "brd-customer-hl_d8e30669-zone-datacenter_proxy1",
                # "password": "9mks7jyv70n1"
                # })
        context = browser #await browser.new_context()
        await context.add_cookies(cookies)

        page = context.pages[0] #await context.new_page()
        await open_browser(page)
        time.sleep(10)
        if await page.is_visible('text=Sign in'):
            await page.click("text=Sign in")

            await page.wait_for_timeout(2000)
            await page.fill('input[name="userid"]', 'tradersalcove@gmail.com')
            await page.click('button[id="signin-continue-btn"]')

            await page.wait_for_timeout(2000)
            await page.fill('input[name="pass"]', 'Golddoor737')
            await page.click('button[id="sgnBt"]')

            await page.wait_for_timeout(2000)
            if await page.is_visible('div.stepupauth-hub-box'):
                await page.click('button[id="send-button"]')

        # saving the cookies to file
        cookies = await context.cookies()
        with open(f'cookies/{cookiefile}', 'w') as file:
            json.dump(cookies, file)

        connection = pymongo.MongoClient('localhost', 27017)
        db = connection['ebay']
        col = db['ebay']
        col.delete_many({"Matches":"No matches found"})
        cur = col.find({"MaxSoldPrice": {"$exists": False},"Matches":{"$ne":"No matches found"},"Matches": { "$exists": True }})
        cur = [i for i in cur]
        print(f"Total search count {len(cur)}")
        for obj in cur:
            time.sleep(random.randint(7, 15))
            print(obj)
            match = obj['Matches']
            nomatch = obj['Matches']
            print(len(match))
            print(len(nomatch))
            if len(match) == 0:
                continue
            prices = []

            shutil.copy(f'mached/{obj["ImageName"]}', f'TrPeak/{obj["ImageName"]}')
            imgPrice = {}
            noimgPrice = {}
            for j in match:
                time.sleep(random.randint(10, 20))
                print(j)
                id = j.split('.')[0]
                file = f'mached/{id}.html'
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                soup = bs(content, 'html.parser')
                h1 = soup.find('h1')
                text = h1.text
                queryLists = [' '.join(text.split(' ')[:i]) for i in range(4, len(text.split(' ')) + 1, 4)]
                plt.imshow(plt.imread(f'mached/{id}.jpg'))
                print(queryLists)
                for qry in queryLists:
                    print(qry)
                    # searching for something
                    queryBox = await page.query_selector('span.textbox.search-input-panel__inputBox')
                    query = await queryBox.query_selector('input.textbox__control')
                    await query.fill(qry)
                    await page.wait_for_timeout(1000)
                    await page.keyboard.press('Enter')
                    await page.wait_for_timeout(1000)
                    await page.click('xpath=/html/body/div[2]/div[6]/div[2]/section/div[1]/span/div/div/div/span/div/div/div[1]/div[1]/span')
                    await page.wait_for_timeout(3000)

                    # selecting all results with their name and links
                    resSec = await page.query_selector('table.static-table__table-content.static-table__table-content-default')
                    try:
                        allres = await resSec.query_selector_all('tr.research-table-row')
                        for i in allres:
                            imglink = await i.query_selector('img.small')
                            img = str(await imglink.get_attribute('src')).replace('//i.', 'https://i.')
                            print(img)
                            imgname = await i.query_selector('div.research-table-row__product-info-name')
                            imgname = await imgname.inner_text()
                            print(imgname)
                            soldval = await i.query_selector('TD.research-table-row__item.research-table-row__totalSalesValue')
                            price = str(await soldval.inner_text()).replace("$", "")
                            print(price)
                            FImgNm = f'++{imgname}++{price}++.jpg'.replace('/', '?')
                            print(FImgNm)
                            if img not in imgPrice:
                                imgPrice[img] = FImgNm
                    except:
                        print('No price found')

            if len(imgPrice) == 0:
                for imag in nomatch:
                    print(imag)
                    noid = imag.split('.')[0]
                    nofile = f'mached/{noid}.html'
                    with open(nofile, 'r', encoding='utf-8') as f:
                        content = f.read()
                    soup = bs(content, 'html.parser')
                    h1 = soup.find('h1')
                    imgname = h1.text
                    pricesect = soup.find('div', class_='x-price-primary')
                    noprice = float(str(pricesect.text).split(' ')[1].replace('$', ''))
                    noimgPrice[imgname] = noprice

                maxPrice = max(noimgPrice.values())
                for gets in noimgPrice.items():
                    if gets[1] == maxPrice:
                        maxKeyword = gets[0]
                print(maxKeyword)
                print(maxPrice)
                col.find_one_and_update({"ImageName": obj['ImageName']}, {'$set': {"MaxSoldPrice": maxPrice, "MaxSoldKeyword": maxKeyword}})

            else:
                if not os.path.exists('TrPeak'):
                    os.mkdir('TrPeak')

                for i in os.listdir('TrPeak'):
                    os.remove('TrPeak/' + i)

                def saveTrPeak(lin):
                    req = requests.get(lin)
                    image = Image.open(BytesIO(req.content))
                    if image.mode == 'WEBP' or image.mode == 'RGBA':
                        image = image.convert('RGB')
                    re_image = image.resize((640, 640))
                    re_image.save(f"TrPeak/{imgPrice[lin]}", 'JPEG')

                with ThreadPoolExecutor(max_workers=50) as executor:
                    executor.map(saveTrPeak, list(imgPrice.keys()))

                custom_config = CustomModel(name=MobilenetV3.name,
                                            model=MobilenetV3(),
                                            transform=MobilenetV3.transform)
                cnn_encoder = CNN(model_config=custom_config)
                image_dir = Path("TrPeak")
                duplicates_cnn = cnn_encoder.find_duplicates(image_dir=image_dir, scores=True)

                output_folder = "TrPeakmached"
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                matches = set()
                for i in duplicates_cnn:
                    if len(duplicates_cnn[i]) > 0 and obj['ImageName'].split('.')[0] in i:
                        print(i)
                        for j in duplicates_cnn[i]:
                            if j[1] > 0.9:
                                matches.add(j[0])
                                shutil.copy(f'TrPeak/{j[0]}', f'{output_folder}/{j[0]}')
                    elif len(duplicates_cnn[i]) == 0:
                        for imag in nomatch:
                            noid = imag.split('.')[0]
                            nofile = f'mached/{noid}.html'
                            with open(nofile, 'r', encoding='utf-8') as f:
                                content = f.read()
                            soup = bs(content, 'html.parser')
                            h1 = soup.find('h1')
                            imgname = h1.text
                            pricesect = soup.find('div', class_='x-price-primary')
                            noprice = float(str(pricesect.text).split(' ')[1].replace('$', ''))
                            noimgPrice[imgname] = noprice

                        maxPrice = max(noimgPrice.values())
                        for gets in noimgPrice.items():
                            if gets[1] == maxPrice:
                                maxKeyword = gets[0]
                        print(maxKeyword)
                        print(maxPrice)
                        col.find_one_and_update({"ImageName": obj['ImageName']}, {'$set': {"MaxSoldPrice": maxPrice, "MaxSoldKeyword": maxKeyword}})
                        break

                if len(matches) == 0:
                    maxPrice = max(noimgPrice.values())
                    for gets in noimgPrice.items():
                        if gets[1] == maxPrice:
                            maxKeyword = gets[0]
                    print(maxKeyword)
                    print(maxPrice)
                    col.find_one_and_update({"ImageName": obj['ImageName']}, {'$set': {"MaxSoldPrice": maxPrice, "MaxSoldKeyword": maxKeyword}})

                else:
                    print(matches)
                    col.find_one_and_update({"ImageName": obj['ImageName']}, {'$set': {"MaxSoldPrice": maxPrice, "MaxSoldKeyword": maxKeyword}})

        await browser.close()

# Running the function
if __name__ == '__main__':
    import asyncio
    asyncio.run(runResearching(cookies))
