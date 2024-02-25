# This module performs a summary for a single offer 
# Input - 1. a link to the page where the details of a single offer, and 
        # 2. path to the target folder for the single offer's documents (later the docs will be loaded from that chosen folder and summarized)
# output - 1. summary as a long string (the main program will then save the text in a desired localization)
         # 2. info on fullfilled or unfullfilled requirements from the user 


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import os
import shutil
import zipfile
from zipfile import ZipFile
import time
from datetime import datetime
import fitz  #pdf text recognition

import subprocess

import read_pdfs

## ## to do - searching for the keywords in the offer's content that could give the information 
## ## on the initial deposit (keywords must be of course in the language of the analysed documents - here it's Polish)
keywords_to_detect = {'wadium', 'akonto', 'forszus', 'gwarancja pieniężna', 'kaucja', 'przedpłata', 'rękojmia', 'zabezpieczenie', 'zadatek', 'zaliczka', 'zastaw'}


# Initializing the Chrome browser 
driver = webdriver.Chrome()

# Webdriver goes to the page containng the list of offers for the Contractor (User) - in this case it is the Orlen's site
# Downloading the visible dynamic content from the browser using Selenium 
link = 'https://connect.orlen.pl/app/outRfx/338906/supplier/status' ### change this line later into elastic input from another program  
driver.get(link)

# Checking the number of the single offer displayed on the site
number_of_donloaded_offer_RAW = driver.find_element(By.TAG_NAME, 'strong').text    

# Removing the forbidden characters 
import re
numer_pobieranej_oferty = number_of_donloaded_offer_RAW.replace('/', '_')
numer_pobieranej_oferty =  re.sub(r'[\\/*?:"<>|]', '', numer_pobieranej_oferty)

print(f"numer pobranego folderu (oczyszczony z ukośników): {numer_pobieranej_oferty}")

# Setting the max waiting time for finding the desired element on the website 
# (here - a "Download" button that initiates the download of the documents to analyze)
wait = WebDriverWait(driver, 10)

# Finding and autoclicking the "Download" button on the page 
documents_download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "pull-right")]')))
documents_download_button.click()
time.sleep(2)

# Establishing the home directory and the Downloads folder path
Home_dir = Path.home()
Downloads_dir = Home_dir.joinpath('downloads')
#print(Downloads_dir)


# Changing the working directory to the folder where this module (summarizer.py) is located 
p = Path(__file__)
os.chdir(str(p.parent)) 


# Current date and time 
#current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Creating a new folder for the offer details and printing a notification (Polish user)
docs_folder_name = Path(f'{numer_pobieranej_oferty}_szczegóły_ofertowe')
print(f"ścieżka z nowymi dokumentami oferty {number_of_donloaded_offer_RAW}: {docs_folder_name}")

#current_offer_path = Path.cwd()
#print(f"folder w którym zapisana jest oferta numer [dodać automatyczny numer oferty]: {current_offer_path}")

# Checking if the folder exists, creating a new one if a folder of this name isn't found
if not docs_folder_name.exists():
    docs_folder_name.mkdir()
    print(f"tworzenie folderu na pobrane szczegóły oferty: {docs_folder_name}")
else:
    print(f"Folder o nazwie {docs_folder_name} już istnieje!")


# Downloading the pdf docs and saving them to a new folder assigned to the particular offer 
# (the offer's ID is automatically attached from the http element from the website)

# Finiding a name of the last downloaded folder (a zip folder is always provided on the website)
list_of_zips_in_downloads = [dlded_folder.path for dlded_folder in os.scandir(str(Downloads_dir)) if zipfile.is_zipfile(dlded_folder)] # Collecting only zipfiles from the "Downloads" folder 
latest_folder = max(list_of_zips_in_downloads, key=os.path.getctime) # pinpointing the last downloaded zipfile - it is our folder with the docs to analyze for the User

# print(f"lista wszystkich znalezionych folderów zip: {list_of_zips_in_downloads}") # detection test
# print(f"ostatni pobrany folder: {latest_folder}") # detection test


# The full path to the target folder where the docs of a single offer will go 
print(f"Ścieżka folderu docelowego: {docs_folder_name}")

# Path to the copied file in the target folder 
dlded_zip_file_name = os.path.basename(latest_folder)
moved_zip_file_path = os.path.join(docs_folder_name, dlded_zip_file_name)

# Moving the downloaded zipfile to the target folder 
if not os.path.exists(moved_zip_file_path):
    shutil.move(latest_folder, docs_folder_name)
    print(f'Plik z Pobranych "{latest_folder}" został przeniesiony do "{docs_folder_name}"')
else:
    print("Plik o takiej samej nazwie już istnieje w folderze docelowym.")

# Changing the directory from the folder with the new zipfile and extraction of docs 
os.chdir(str(docs_folder_name)) 

    # Grabbing the list of the files and folders in the current folder 
fold_contents = os.scandir(os.getcwd())

    # finding the name first folder with .zip extension (if it exists) and displaying that name
    # thhe loop checks for zipfiles 
for file in fold_contents:
    if file.is_file() and file.name.endswith('.zip'):
        zip_file_name = file.name
        print(f"Znaleziono plik zip o nazwie: {zip_file_name} - wypakowuję...")
        break  # break after finding the first zipfile 

subprocess.run(['python', 'read_pdfs.py'])
read_pdfs.read_pdf_files_text()

###with zipfile.ZipFile(zip_file_name, 'r') as zip_ref: ### We can read the text from pdf's inside the .zip without unzipping
    ###zip_ref.extractall(os.getcwd())

# text extraction from each page of the docs 
"""    
text = ""
path = "Your_scanned_or_partial_scanned.pdf"

doc = fitz.open(path)
for page in doc:
    text += page.get_text()()
 """

wait2 = input() #dummy variable