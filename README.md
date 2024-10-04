# EbayPostcardHunt
Sell your Postcards at a profitable price when you don't know what you call it and how much it will get sold on. 
## Requirements
- Miniconda3
- MongoDB
- Ebay account + Developer's Account
## Installation
~ Run ```python FolderSetup.py``` to setup folder structure.\
~ Installation of ```Imagededup``` library may throw errors so run 
```bash
git clone https://github.com/idealo/imagededup.git 
cd imagededup
pip install "cython>=0.29"
python setup.py install
```
~ You will require to collect cookies for the first time from your browser for login credentials of ebay + ebay developer account so visit [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?utm_source=ext_app_menu) and install it. \
~ After installation visit [Ebay](https://www.ebay.com) and login to your account. Click on Cookie-Editor Extension click on ```Export``` then select ```Export as JSON```. Save the cookies in ```cookies.txt``` file \
~ Visit [Ebay Developer](https://developer.ebay.com) and login to your account. After logging to developer account visit [Get Token](https://www.developer.ebay.com/my/auth/?env=production&index=0&auth_type=oauth). Create an App with name then create auth for ```Production Environment``` -> Select ```Auth OAuth (new security)``` -> Click on ```Sign in to Production for OAuth``` . Click on ```Cookie-Editor``` Extension click on ```Export``` then select ```Export as JSON``` . Save the cookies in ```Authcookies.txt```\

## Usage
~ Place PDF files with scanned images in ```pdfs``` folder.\
~ Run the following commamd to extract images from PDFs for the fresh batch of pdfs which have scanned images. If you already have extracted images then you can place the images in ```pdf_imgs``` folder. 
```bash 
python extractImages.py
```  
~ Run the following command to get the matches from the images in ```pdf_imgs``` folder , you will see the obtained results in ```matched``` folder and in MongoDB , you can view the results in ```MongoDB Compas```. 
```bash
python matchFinder.py
```
~ Run the following command to get the prices of the matched images from Ebay TerePeak Research work. You will see the obtained results in ```MongoDB Compas```. 
```bash
python TerePeakMatchAsync.py
```
~ ```Finally``` You can see the matched images on ebay which were either sold before or are currently on sale. You can see the prices of the PostCards with the Keyword with which it was listed on ebay and can sell your images at a profitable price.
