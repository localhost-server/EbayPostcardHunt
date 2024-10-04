import os

reqFolders=['down_imgs','htmls','TrPeak','TrPeakmached','mached','pdf_imgs','pdfs','re_imgs']

# checking if all folders exist or not
def checkFolders():
    for folder in reqFolders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"{folder} folder created")
        else:
            print(f"{folder} folder already exists")

checkFolders()
