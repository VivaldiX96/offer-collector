#moduł wykonujący pojedyncze streszczenie dla pojedyczej oferty
# input - link do strony na której są szczegóły oferty oraz ścieżka folderu docelowego (na razie zakładam że będzie to folder, w którym ten moduł będzie umieszczony); potem będzie pobrany z tej strony dokument i sczytany z niego tekst
# output - streszczenie oferty w formie tekstu (główny program będzie potem zapisywał ten tekst jako odpowiedni dokument w odpowiedniej lokacji), 
# spełnione lub niespełnione kryteria oferty określone przez użytkownika


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

## ## do zrobienia - wyszukiwanie informacji o wadium przy czytaniu treści oferty
slowa_kluczowe_wadium = {'wadium', 'akonto', 'forszus', 'gwarancja pieniężna', 'kaucja', 'przedpłata', 'rękojmia', 'zabezpieczenie', 'zadatek', 'zaliczka', 'zastaw'}


# Inicjalizacja przeglądarki (w tym przypadku Google Chrome)
driver = webdriver.Chrome()

# Przechodzimy na stronę, która zawiera szczegóły ofert - tutaj strona Orlenu; zeskanowanie widocznej treści z użyciem Selenium

link = 'https://connect.orlen.pl/app/outRfx/338906/supplier/status' #zmienić linijkę na elastyczny input z drugiego programu
driver.get(link)


numer_pobieranej_oferty_raw = driver.find_element(By.TAG_NAME, 'strong').text #sprawdza numer oferty wyświetlający się na stronie

# Usunięcie niedozwolonych znaków
import re
numer_pobieranej_oferty = numer_pobieranej_oferty_raw.replace('/', '_')
numer_pobieranej_oferty =  re.sub(r'[\\/*?:"<>|]', '', numer_pobieranej_oferty)

print(f"numer pobranego folderu (oczyszczony z ukośników): {numer_pobieranej_oferty}")

# Ustawiamy maksymalny czas oczekiwania na znalezienie elementu (np. przycisku "Pokaż więcej")
wait = WebDriverWait(driver, 10)

#znalezienie na stronie i kliknięcie przycisku pobierania - pobranie dokumentów oferty

documents_download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "pull-right")]')))
documents_download_button.click()
time.sleep(2)

#ustalenie lokalizacji domowej i folderu downloads
Home_dir = Path.home()
Downloads_dir = Home_dir.joinpath('downloads')
#print(Downloads_dir)





#zmiana foldru roboczego na folder, w którym jest summarizer.py
p = Path(__file__)
os.chdir(str(p.parent)) 


# Aktualna data i godzina
#aktualna_data_i_godzina = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Utworzenie pełnej nazwy folderu
#pelna_nazwa_folderu = f'{nazwa_folderu}_{aktualna_data_i_godzina}' ### czy data i godzina jest niezbędna?

#utworzenie nowego folderu na pobrane szczegóły oferty

docs_folder_name = Path(f'{numer_pobieranej_oferty}_szczegóły_ofertowe')
print(f"ścieżka z nowymi dokumentami oferty {numer_pobieranej_oferty_raw}: {docs_folder_name}")




#current_offer_path = Path.cwd()
#print(f"folder w którym zapisana jest oferta numer [dodać automatyczny numer oferty]: {current_offer_path}")

# Sprawdź czy folder istnieje, jeśli nie to utwórz
if not docs_folder_name.exists():
    docs_folder_name.mkdir()
    print(f"tworzenie folderu na pobrane szczegóły oferty: {docs_folder_name}")
else:
    print(f"Folder o nazwie {docs_folder_name} już istnieje!")


# pobranie dokumentów pdf i zapisanie ich do nowego folderu z tytułem z numerem zapytania i datą pojawienia się zapytania 
# (numer oferty jest automatycznie dołączany przez stronę przy pobieraniu, nie trzeba go zaciągać z danych ani nadawać)

#znajdywanie nazwy ostatniego pobranego folderu, a nie pliku (ze strony pobierany jest folder z plikami a nie plik)
list_of_zips_in_downloads = [dlded_folder.path for dlded_folder in os.scandir(str(Downloads_dir)) if zipfile.is_zipfile(dlded_folder)] #zebranie tylko folderów zipfile, a nie plików, z Pobranych
latest_folder = max(list_of_zips_in_downloads, key=os.path.getctime) #namierzenie ostatniego pobranego folderu - nasz folder z dokumentami
print(f"lista wszystkich znalezionych folderów zip: {list_of_zips_in_downloads}")
print(f"ostatni pobrany folder: {latest_folder}")


# Pełna ścieżka do folderu docelowego
print(f"Ścieżka folderu docelowego: {docs_folder_name}")

#ścieżka do skopiowanego pliku w folderze docelowym
dlded_zip_file_name = os.path.basename(latest_folder)
moved_zip_file_path = os.path.join(docs_folder_name, dlded_zip_file_name)

# Przeniesienie folderu
if not os.path.exists(moved_zip_file_path):
    shutil.move(latest_folder, docs_folder_name)
    print(f'Plik z Pobranych "{latest_folder}" został przeniesiony do "{docs_folder_name}"')
else:
    print("Plik o takiej samej nazwie już istnieje w folderze docelowym.")

# przejście do folderu z nowym plikiem zip i ekstrakcja dokumentów
os.chdir(str(docs_folder_name)) 

    # Pobranie listy plików i katalogów w bieżącym folderze
fold_contents = os.scandir(os.getcwd())

    # Wyłuskanie nazwy pierwszego folderu z rozszerzeniem ".zip" (jeśli istnieje) i wyświetlenie jej; 
    # Pętla przeszukuje po kolei zawartość aż trafi na plik zip
for file in fold_contents:
    if file.is_file() and file.name.endswith('.zip'):
        zip_file_name = file.name
        print(f"Znaleziono plik zip o nazwie: {zip_file_name} - wypakowuję...")
        break  # Przerwij pętlę po znalezieniu pierwszego pasującego pliku zip

subprocess.run(['python', 'read_pdfs.py'])
read_pdfs.read_pdf_files_text()

###with zipfile.ZipFile(zip_file_name, 'r') as zip_ref: ### można bez wypakowania odczytać tekst z pdfów wewnątrz pliku zip
    ###zip_ref.extractall(os.getcwd())

#ekstrakcja tekstu z kolejnych stron kolejnych dokumentów
"""    
text = ""
path = "Your_scanned_or_partial_scanned.pdf"

doc = fitz.open(path)
for page in doc:
    text += page.get_text()()
 """

##przykładowa wzmianka o wadium:
##XIII. Zabezpieczenie
##W prowadzonym postępowaniu Zamawiający nie wymaga wniesienia zabezpieczenia należytego
##wykonania umowy.

czekaj2 = input()

#ostatni output:
#DevTools listening on ws://127.0.0.1:60935/devtools/browser/41aadc52-8239-4134-82bf-19269103b596
#numer pobranego folderu: ELOG/2/000838/24
#ścieżka current name: folder_z_dokumentami_oferty_11111
#tworzenie folderu na pobrane szczegóły oferty: folder_z_dokumentami_oferty_11111
#lista wszystkich znalezionych folderów zip: ['C:\\Users\\antek\\downloads\\ELOG_2_000838_24 (1).zip', 'C:\\Users\\antek\\downloads\\ELOG_2_000838_24 (2).zip', 'C:\\Users\\antek\\downloads\\ELOG_2_000838_24 (3).zip', 'C:\\Users\\antek\\downloads\\ELOG_2_000838_24 (4).zip', 'C:\\Users\\antek\\downloads\\ELOG_2_000838_24 (5).zip', 'C:\\Users\\antek\\downloads\\ELOG_2_000838_24.zip', 'C:\\Users\\antek\\downloads\\obrony ITLIMS  październik 2019_wersja 4.xlsx', 'C:\\Users\\antek\\downloads\\Ogłoszenie-poszukiwani-kandydaci_1.G.10.docx', 'C:\\Users\\antek\\downloads\\OriginThinSetup.exe', 'C:\\Users\\antek\\downloads\\PainterEssentials6.exe', 'C:\\Users\\antek\\downloads\\PARTserver02018112218592328921031192d056f.zip', 'C:\\Users\\antek\\downloads\\PenTablet_5.3.5-3.exe', 'C:\\Users\\antek\\downloads\\powtarzanie semetru-dzienne (1).doc', 'C:\\Users\\antek\\downloads\\powtórzenie M2 lato 18.docx', 'C:\\Users\\antek\\downloads\\pre.zip', 'C:\\Users\\antek\\downloads\\redfive.zip', 'C:\\Users\\antek\\downloads\\saved-by-zero.zip', 'C:\\Users\\antek\\downloads\\Tworzenie swoich tekstów - lista.ods', 'C:\\Users\\antek\\downloads\\Wiadomość_CZITT_30.09.docx']
#ostatni pobrany folder: C:\Users\antek\downloads\ELOG_2_000838_24 (5).zip
#Ścieżka folderu docelowego: folder_z_dokumentami_oferty_11111
#Pobrany folder "C:\Users\antek\downloads\ELOG_2_000838_24 (5).zip" został przeniesiony do "folder_z_dokumentami_oferty_11111"
#obecna ścieżka robocza: C:\Coding\WebScraper\folder_z_dokumentami_oferty_11111. Wypakowuję folder zip...