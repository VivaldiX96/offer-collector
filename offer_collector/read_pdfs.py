# Module for pdf reading - it is supposed to detect which pdf's contain text and which don't and analyze the ones with raster graphics 
# It returns the read pdf's in text format 


from pathlib import Path
import os
import io
import zipfile
import fitz # PyMuPDF, library for reading text from pdf's

#import summarizer



text_for_AI_to_read = None


## reads text from a single pdf. WARNING: works only for specific cases when there is a pdf directly in the first layer inside the zipfile
## works in the folder: C:\Coding\WebScraper\examples\scrapped_files\ELOG200083824_szczegoly_ofertowe\1_Opracowanie_dokumentacji
def readPdfFilesText():
    print(f"uruchamiam moduł {__name__}")

    # chacking that the module runs in the folder created for the files which have to be read 
    #os.chdir(str(summarizer.docs_folder_name)) 

    # Getting the list of the files and folders in the current directory 
    fold_contents = os.scandir(os.getcwd())

        # Getting the name of the first folder with .zip extension (if it exists) and displaying it  
        # The loop searches the content until it finds a zipfile  
    for file in fold_contents:
        if file.is_file() and file.name.endswith('.zip'):
            zip_file_name = file.name
            zip_file_path = file.path
            print(f"Znaleziono plik zip o nazwie: \"{zip_file_name}\" - czytam tekst zawartych dokumentów...") 
            # Opening the zipfile 
            with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                # Going through all the files in the zip archive 
                for file_info in zip_file.infolist():
                    # Checking if the file is a pdf
                    if file_info.filename.endswith(".pdf"):
                        # Opening the PDF file without unzipping  
                        with zip_file.open(file_info) as pdf_file:
                            # Reading the data from the PDF file
                            pdf_data = io.BytesIO(pdf_file.read())
                            # Extraction of text from the PDF file
                            doc = fitz.open("pdf", pdf_data)
                            text = ""
                            for page_number in range(doc.page_count):
                                page = doc.load_page(page_number)
                                text += page.get_text("text")
                            print("Tekst z pliku PDF:", text)
                            global text_for_AI_to_read
                            text_for_AI_to_read = text
                    #else if file_info.filename.endswith(".zip"):   
                 
            break  # Break the loop after finding the first matching zipfile  
        #!! Change - find all zip's 

readPdfFilesText()

# pdf = fitz.open(zip_file_path)
