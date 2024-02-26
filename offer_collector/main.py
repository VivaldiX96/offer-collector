
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
import os

# import webscraper # <- importing the second module of the program 

REPLICATE_API_TOKEN = 'abc' #placeholder

URL = 'https://connect.orlen.pl/servlet/HomeServlet' #the URL of the page with all the newest offers to collect for the User

DETAILED_INSTRUCTIONS = None #custom requests from the User - extra feature to be developed in the future

# At the beginning add the options in radio buttons to  

instr_options = {
                 "DEFAULT": "detect_deposit_and_reqs", # detecting info about an initial deposit or warranty,   wykrywanie informacji czy jest wymagane wadium, gwarancja, 
                                                       # and also if there are any extra requirements regarding the contractor 
                                                       # including similar projects created earlier or special qualifications/certificates
                 
                 "SUMMARY": "offer summary", # a brief summary of the documents 
                 
                 "GPT_DETAILS": DETAILED_INSTRUCTIONS # detailed instructions from the User to be implemented by AI -
                                                      #  - particularly, finding custom details of information on demand 
                }


#options = webdriver.ChromeOptions()
#options.add_experimental_option("detach", True)



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



def BuildingOffersList():
 
    offers = driver.find_elements(By.CLASS_NAME, 'demand-item')

    print(f"Liczba ofert: {len(offers)}")

    offers_table = []

    for offer in offers:
        
        offer_number = offer.find_element(By.CLASS_NAME, 'demand-item-details-number').text
        title = offer.find_element(By.CLASS_NAME, 'demand-item-details-name').text
        cathegory = offer.find_element(By.CLASS_NAME, 'demand-item-details-category').text
        link_to_details = offer.find_element(By.CLASS_NAME, 'demand-item-to-details').get_attribute("href")
        time_remaining = offer.find_element(By.CLASS_NAME, 'demand-item-time').text

        # Polish names for the headers of the table in the sheet that the User will be able to read
        offer_object = {
            'numer': offer_number,
            'tytul': title,
            'kategoria': cathegory,
            'link': link_to_details,
            'pozostaly czas': time_remaining
        }
        offers_table.append(offer_object)

    offers_df = pd.DataFrame(offers_table)

    # Filtering the offer objects by their cathegory (only the cathegory "Documentation of technical projects" is of interest to our User)
    offers_df = offers_df[offers_df.kategoria.str.contains('Dokumentacja - projekty techniczne')]
    print(f"Liczba ofert z kategorii \"Wykonanie projektów\": {len(offers_df.index)}")
    print(offers_df)
    return offers_df

if __name__ == "__main__":

    orlen_expandclicker()

    webscraped_offers_df = BuildingOffersList()


    # establishing the path where the executed .py file is located and changing the working directory to that current path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)


    ### print(f"ścieżka folderu roboczego: {Path.cwd()}") ### - these two lines are to be activated for control/testing purposes
    ### print(f"ścieżka pliku Python: {Path(__file__)}") ### - they let check, where the program is located and where it writes the files


    # the name of the new folder for a csv file with the list of offers that the User can view
    folder_path = 'folder_na_csv'


    # Checking if the folder exists - if not, creating it 
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder o nazwie {folder_path} jeszcze nie istnieje w katalogu roboczym; \ntworzenie nowego folderu {folder_path}...")


    # Naming the excel file holding the gathered offers, creating the path where the file will be located
    excel_doc_filaname = 'Arkusz_ofert.xlsx'
    excel_doc_path = os.path.join(folder_path, excel_doc_filaname)


    # importing of the recent sheet, if it exists
    if os.path.isfile(excel_doc_path):
        # loading the Excel file to the Dataframe object 
        recent_webscraped_offers_df = pd.read_excel(excel_doc_path)
        print("Aktualizacja pliku excel...")

        #### newdf=pd.concat([recent_webscraped_offers_df, webscraped_offers_df]).drop_duplicates(keep=False)  # code for obtaining the difference between the new and the old Dataframe 

        # merging the old Dataframe sheet with the new one
        webscraped_offers_df_new_rows = webscraped_offers_df.merge(recent_webscraped_offers_df, on='numer', how='outer', indicator=True)
        print(f"Nowy arkusz z indykatorami dla sprawdzenia: {webscraped_offers_df_new_rows}")
        
        # Choosing only new rows
        new_rows = webscraped_offers_df_new_rows.query('_merge == "left_only"').drop(columns=['_merge'])

        # Resulting DataFrame:
        print(f"nowe oferty: \n{new_rows}")

        # New DataFrame without the indicator column, which will be exported to Excel file: 
        webscraped_offers_df = webscraped_offers_df.merge(recent_webscraped_offers_df, on='numer', how='outer', indicator=False)

        print(f"Nowy plik excel: {webscraped_offers_df}")

    else:
        # Displaying the info about the absence of the last sheet and about the location where the new one will be created 
        print(f"Plik o nazwie {excel_doc_filaname} jeszcze nie istnieje w folderze w katalogu roboczym; \ntworzenie nowego pliku w folderze {folder_path}...")


    # Saving the DataFrame to the Excel file in the chosen path 
    webscraped_offers_df.to_excel(excel_doc_path, index=False, sheet_name='Initial_Offers')
    excel_doc_path_abs = os.path.abspath(excel_doc_path)
    print(f"Arkusz Excel został utworzony w folderze {folder_path}.\nŚcieżka pliku: {excel_doc_path_abs}")

    # Path of the CSV file in the newly created folder
    file_path = os.path.join(folder_path, 'offers_table.csv')
    absolute_path = os.path.abspath(file_path)
    #print(f"ścieżka pliku: {absolute_path}")

    # Saving the list to a CSV file 
    # webscraped_offers_df.to_csv(file_path, index=False)
    webscraped_offers_df.to_csv(file_path, mode='w', encoding='utf-8-sig', index=False) 
    print(f"Plik CSV został utworzony w folderze {folder_path}.\nŚcieżka pliku: {absolute_path}")


    # Append to an existing Excel sheet 
    #with pd.ExcelWriter('arkusz_ofert.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:   
        # webscraped_offers_df.to_excel(writer, sheet_name='Initial_Offers2') # --> change the code so that it moves the older lines down to make space for the new ones



    wait = input() # a dummy task to prevent the browser from closing on it's own


