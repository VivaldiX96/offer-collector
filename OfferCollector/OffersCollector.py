
# THE PLAN OF THE PROGRAM WRITTEN FOR GATHERING DATA FROM THE PAGE https://connect.orlen.pl/servlet/HomeServlet:

    # - A clicker of the "Show more" button on the webscraped page  ✓
    # - Creating the list of all offers and saving it in a csv file  ✓
        # - Optional - enabling the cathegory filter on the website so that less incompatible offers are displayed and delivered to the program for analysis (preliminarily - solved with a filter affecting the Dataframe object of all offers taken from the source website) 
    # - Entering the sub-website dedicated to a chosen offer  ✓
        # - Downloading the documents (pdf, doc, etc.) with a detailed description of a single offer  ✓
        # - Reading the text from a single offer  ✓
        # - Detecting the keywords from a chosen set in the downloaded documents - could be done with a speech processing program using linguistic functions 
        # - Sending the description of the offer to LLM for summarization 

        # - Filtering obvious negligible offers based on their titles or cathegories on the website providing the offers for reducing the number of the resulting queries sent to the LLM


    # - Setting the constant criterions of assessment for ChatGPT and a constant command to return "0" or "1"  ✓
    # - Sending the data from one offer to ChatGPT - Offer_collector.py (main program)
    # - Sending offers marked with "1" to the folder of offers to consider for the end user


# !!! Installed packages (install them in the container - the same set is in the requirements.txt file):
    # pip install selenium==4.16.0
    # https://googlechromelabs.github.io/chrome-for-testing/ - https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/win64/chromedriver-win64.zip
    # pip install openpyxl==3.1.2
    
    # node-v20.10.0-x64
    # pip install --upgrade pymupdf - for text recognition in pdf's 
    # pip install PyMuPDF==1.23.9 - libraries for PDF's reading by the program; >>> in the .py code modules - "import fitz" (this imports the pymupdf library) 
    # pip install openai==0.28.0 - for communication with ChatGPT 
    # pip install streamlit==1.30.0 - for creating the UI with the option of custom instruction for the AI Assistant  
    # pip install googletrans==4.0.0rc1 - for translations of documents' texts from source language to English to supply the text to interpret by LLAMA2 in the module LLAMA2_query_generator.py 
    # pip install replicate==0.23.1 - for interactions with AI from the program instead of hand typing 
    # pip install requests==2.31.0
    # pip install docker==7.0.0 - a library to connect with docker like with docker commands, needed to send queries to an app in a container and reading answers from it (a dockerized LLM model for example)
    # pip install operagxdriver==0.10
    # https://github.com/docker/docker-py
    
    # Libraries that are not used yet - consider installing for adding extra functionalities:
    # pip install beautifulsoup4 - not used, for now selenium is sufficient for the webscraping purposes
    # pip install pydocker - another way to connect with AI in a container
    # pip install pillow - to detect images and text in the images, for example to read any scanned documents
    # pip install python-docx - a library to save documents with a desired style or formatting
    # pip install pyttsx3 - for speech recognition
    # pip install SpeechRecognition - -||-

### Current scope of issues to check: test which tokenizer for LLAMA 2 handles Polish text the best, check how to increase or go around the character number limit in the chat (maybe a suitable tokenizer or langchain might help?)   
### some tips on supplying the system prompts:  https://www.youtube.com/watch?v=PqcNqyd13Kw
### fine-tuning for language models:  https://www.youtube.com/watch?v=ThKWQcyQXF8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import streamlit as st
import pathlib
import posixpath
import pandas as pd

# import webscraper # <- importing the second module of the program 

REPLICATE_API_TOKEN = 'abc' #placeholder

detailed_instructions = None #custom requests from the User - extra feature to be developed in the future

# At the beginning add the options in radio buttons to  

instr_options = {
                 "DEFAULT": "detect_deposit_and_reqs", # detecting info about an initial deposit or warranty,   wykrywanie informacji czy jest wymagane wadium, gwarancja, 
                                                       # and also if there are any extra requirements regarding the contractor 
                                                       # including similar projects created earlier or special qualifications/certificates
                 
                 "SUMMARY": "offer summary", # a brief summary of the documents 
                 
                 "GPT_DETAILS": detailed_instructions # detailed instructions from the User to be implemented by AI -
                                                      #  - particularly, finding custom details of information on demand 
                }





#options = webdriver.ChromeOptions()
#options.add_experimental_option("detach", True)

URL = 'https://connect.orlen.pl/servlet/HomeServlet'

# Initializing the Chrome browser 
driver = webdriver.Chrome()

# Webdriver goes to the page containng the list of offers for the Contractor (User) - in this case it is the Orlen's site
# Downloading the visible dynamic content from the browser using Selenium 
driver.get(URL)


# Setting the maximum wait time to find the "Show More" button 
# (the list of offers has to be expanded to enable to grab all necessary data) 
wait = WebDriverWait(driver, 10)

def orlen_expandclicker():
    for licznik in range(1, 6):  # a preliminary test version with 5x click of the "Show More" button - change to expanding till reaching offer gathered during the last operation of this program
        show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "link-btn") and contains(@class, "link-load-more")]')))
        show_more_button.click()
        time.sleep(3)

orlen_expandclicker()

# webscraper() # start


 
oferty = driver.find_elements(By.CLASS_NAME, 'demand-item')

print(f"Liczba ofert: {len(oferty)}")

offers_table = []

for oferta in oferty:
    
    numer_oferty = oferta.find_element(By.CLASS_NAME, 'demand-item-details-number').text
    tytul_oferty = oferta.find_element(By.CLASS_NAME, 'demand-item-details-name').text
    kategoria_oferty = oferta.find_element(By.CLASS_NAME, 'demand-item-details-category').text
    link_do_szczegolow = oferta.find_element(By.CLASS_NAME, 'demand-item-to-details').get_attribute("href")
    pozostaly_czas = oferta.find_element(By.CLASS_NAME, 'demand-item-time').text
     
    offer_object = {
        'numer': numer_oferty,
        'tytul': tytul_oferty,
        'kategoria': kategoria_oferty,
        'link': link_do_szczegolow,
        'pozostaly czas': pozostaly_czas
    }
    offers_table.append(offer_object)

Orlen_df = pd.DataFrame(offers_table)

# Filtering the offer objects by their cathegory (only Documentation of technical projects interests our User)
Orlen_df = Orlen_df[Orlen_df.kategoria.str.contains('Dokumentacja - projekty techniczne')]
print(f"Liczba ofert z kategorii \"Wykonanie projektów\": {len(Orlen_df.index)}")
print(Orlen_df)


import os


# establishing the path where the executed .py file is located and changing the working directory to that current path
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


### print(f"ścieżka folderu roboczego: {Path.cwd()}") ### - these two lines are to be activated for control/testing purposes
### print(f"ścieżka pliku Python: {Path(__file__)}") ### - they let check, where the program is located and where it writes the files


# the name of the new folder for a csv file with the list of offers
folder_path = 'folder_na_csv'


# Checking if the folder exists - if not, creating it 
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder o nazwie {folder_path} jeszcze nie istnieje w katalogu roboczym; \ntworzenie nowego folderu {folder_path}...")


# Naming the excel file holding the gathered offers, creating the path where the file will be located
nazwa_pliku_excel = 'Arkusz_ofert.xlsx'
sciezka_do_pliku_excel = os.path.join(folder_path, nazwa_pliku_excel)


# importing of the recent sheet, if it exists
if os.path.isfile(sciezka_do_pliku_excel):
    # loading the Excel file to the Dataframe object 
    Poprzedni_Orlen_df = pd.read_excel(sciezka_do_pliku_excel)
    print("Aktualizacja pliku excel...")

    #### newdf=pd.concat([Poprzedni_Orlen_df, Orlen_df]).drop_duplicates(keep=False)  # code for obtaining the difference between the new and the old Dataframe 

    # merging the old Dataframe sheet with the new one
    Orlen_df_nowe_rzedy = Orlen_df.merge(Poprzedni_Orlen_df, on='numer', how='outer', indicator=True)
    print(f"Nowy arkusz z indykatorami dla sprawdzenia: {Orlen_df_nowe_rzedy}")
    
    # Choosing only new rows
    nowe_rzedy = Orlen_df_nowe_rzedy.query('_merge == "left_only"').drop(columns=['_merge'])

    # Resulting DataFrame:
    print(f"nowe oferty: \n{nowe_rzedy}")

    # New DataFrame without the indicator column, which will be exported to Excel file: 
    Orlen_df = Orlen_df.merge(Poprzedni_Orlen_df, on='numer', how='outer', indicator=False)

    print(f"Nowy plik excel: {Orlen_df}")

else:
    # Displaying the info about the absence of the last sheet and about the location where the new one will be created 
    print(f"Plik o nazwie {nazwa_pliku_excel} jeszcze nie istnieje w folderze w katalogu roboczym; \ntworzenie nowego pliku w folderze {folder_path}...")


# Saving the DataFrame to the Excel file in the chosen path 
Orlen_df.to_excel(sciezka_do_pliku_excel, index=False, sheet_name='Initial_Offers')
sciezka_do_pliku_excel_abs = os.path.abspath(sciezka_do_pliku_excel)
print(f"Arkusz Excel został utworzony w folderze {folder_path}.\nŚcieżka pliku: {sciezka_do_pliku_excel_abs}")

# Path of the CSV file in the newly created folder
file_path = os.path.join(folder_path, 'offers_table.csv')
absolute_path = os.path.abspath(file_path)
#print(f"ścieżka pliku: {absolute_path}")

# Saving the list to a CSV file 
# Orlen_df.to_csv(file_path, index=False)
Orlen_df.to_csv(file_path, mode='w', encoding='utf-8-sig', index=False) 
print(f"Plik CSV został utworzony w folderze {folder_path}.\nŚcieżka pliku: {absolute_path}")


# Append to an existing Excel sheet 
#with pd.ExcelWriter('arkusz_ofert.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:   
    # Orlen_df.to_excel(writer, sheet_name='Initial_Offers2') # --> change the code so that it moves the older lines down to make space for the new ones



wait = input() # a dummy task to prevent the browser from closing on it's own


