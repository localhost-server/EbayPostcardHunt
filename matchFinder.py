""" It's Always necessary to get the Auth Token before running the main program."""
import subprocess
subprocess.run(["python", "getAuthToken.py"])
subprocess.run(["python", "FolderSetup.py"])


""" Importing the necessary libraries """
import requests
import base64
import subprocess
import os
import shutil
import matplotlib.pyplot as plt
from pathlib import Path
import pymongo
from imagededup.methods import CNN
from imagededup.utils import CustomModel
from imagededup.utils.models import MobilenetV3

""" Defining some function """
# Convert the image to base64
def image_to_base64(image_path):
    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Read the binary data
        image_data = image_file.read()
        # Encode the binary data to base64
        base64_encoded_data = base64.b64encode(image_data)
        # Convert the base64 bytes to a string
        base64_string = base64_encoded_data.decode('utf-8')
    return base64_string

def get_base(n):
    # return f'https://api.ebay.com/buy/browse/v1/item_summary/search?q=drone&limit={200 if n>=200 else n}'
    return f'https://api.ebay.com/buy/browse/v1/item_summary/search_by_image?&limit={200 if n>=200 else n}&category_ids=914&&aspect_filter=categoryId:262041'


def get_headers(production_oauth):
    return {"Authorization":f"Bearer {production_oauth}",
            # "X-EBAY-C-MARKETPLACE-ID":"EBAY_US",
            "X-EBAY-C-ENDUSERCTX":"affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>",
            "Content-Type":"application/json"}


# reading the token from file named token.txt
with open('token.txt', 'r') as file:
    production_oauth = file.read()

# loading all the images
imagesInFolder=os.listdir('re_imgs')
# connecting to database
connection=pymongo.MongoClient('localhost',27017)
db=connection['ebay']
col=db['ebay']
col.delete_many({"Matches":{"$exists":False}})

for img in  imagesInFolder:
    
    if col.find_one({'ImageName':img}):
        print(f"Already searched {img}")
        continue
    else:
        col.insert_one({'ImageName':img})
    print(img)
    base64_string = image_to_base64(f're_imgs/{img}')
    req=requests.post(get_base(200), headers=get_headers(production_oauth) ,json={"image":base64_string})
    json_data=req.json()
    searched_links=[]
    try:
        searched_links+=[j['itemWebUrl'] for j in json_data['itemSummaries']]
        print("Getting Url List")
        while 'next' in json_data.keys():
            # print(len(searched_links),json_data['next'])
            searched_links+=[i['itemWebUrl'] for i in json_data['itemSummaries']]
            next_req=req=requests.post(json_data['next'], headers=get_headers(production_oauth) ,json={"image":base64_string})
            json_data=req.json()
    except KeyError:
        print("No matches found")
        subprocess.run(["python", "getAuthToken.py"])
        with open('token.txt', 'r') as file:
            production_oauth = file.read()
        req=requests.post(get_base(200), headers=get_headers(production_oauth) ,json={"image":base64_string})
        json_data=req.json()
        searched_links+=[j['itemWebUrl'] for j in json_data['itemSummaries']]
        print("Getting Url List")
        while 'next' in json_data.keys():
            # print(len(searched_links),json_data['next'])
            searched_links+=[i['itemWebUrl'] for i in json_data['itemSummaries']]
            next_req=req=requests.post(json_data['next'], headers=get_headers(production_oauth) ,json={"image":base64_string})
            json_data=req.json()
        # continue

    # saving the links
    with open('searched_links.txt', 'w') as file:
        for link in searched_links:
            file.write(link+'\n')
            
    print("Downloading images")
    # Running the script to download the images
    subprocess.run(["python", "downImages.py"])

    print(f"Links Scraping done \nTotal links found: {len(set(searched_links))}")
    shutil.copy(f're_imgs/{img}', f'down_imgs/{img}')

    print("Finding Matches")
    custom_config = CustomModel(name=MobilenetV3.name,
                                model=MobilenetV3(),
                                transform=MobilenetV3.transform)
    cnn_encoder = CNN(model_config=custom_config)
    image_dir=Path("down_imgs")
    duplicates_cnn = cnn_encoder.find_duplicates(image_dir=image_dir, scores=True)

    output_folder = "mached"

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # removing all saved images
    # for i in os.listdir('mached'):
    #     os.remove(f'mached/{i}')
    matches=set()
    for i in duplicates_cnn:
        if len(duplicates_cnn[i])>0 and img.split('.')[0] in i:
            print(i)
            for j in duplicates_cnn[i]:
                if j[1]>0.9:
                    matches.add(j[0])
                    shutil.copy(f'down_imgs/{j[0]}', f'mached/{j[0]}')
                    html_name=f"{j[0].split('.')[0]}.html"
                    # print(html_name)
                    shutil.copy(f'htmls/{html_name}', f'mached/{html_name}')
            col.find_one_and_update({"ImageName":img},{'$set':{"Matches":list(matches)}})
            shutil.copy(f'down_imgs/{img}', f'mached/{img}')
            
    if len(matches)==0:
        print("No matches found")
        col.find_one_and_update({"ImageName":img},{'$set':{"Matches":"No matches found"}})
        os.remove(f're_imgs/{img}')

    print("---------------------------------------++++++++++++++++++++++Matches found++++++++++++++++++++++---------------------------------------\n\n\n")
