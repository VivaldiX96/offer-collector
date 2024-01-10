#moduł wykonujący pojedyncze streszczenie dla pojedyczej oferty
# input - link do strony na której są szczegóły oferty oraz ścieżka folderu docelowego (na razie zakładam że będzie to folder, w którym ten moduł będzie umieszczony); potem będzie pobrany z tej strony dokument i sczytany z niego tekst
# output - streszczenie oferty w formie tekstu (główny program będziepotem zapisywał ten tekst jako odpowiedni dokument w odpowiedniej lokacji)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import os
import shutil
import zipfile
import time

# Inicjalizacja przeglądarki (w tym przypadku Google Chrome)
driver = webdriver.Chrome()

# Przechodzimy na stronę, która zawiera szczegóły ofert - tutaj strona Orlenu; zeskanowanie widocznej treści z użyciem Selenium

link = 'https://connect.orlen.pl/app/outRfx/339645/supplier/status' #zmienić linijkę na elastyczny input z drugiego programu
driver.get(link)


download_link = driver.find_element(By.CLASS_NAME, 'pull-right').get_attribute("href")
folder_name = os.path.basename(download_link)
print(f"nazwa pobranego folderu:{folder_name}")

# Ustawiamy maksymalny czas oczekiwania na znalezienie elementu (np. przycisku "Pokaż więcej")
wait = WebDriverWait(driver, 10)

#znalezienie dokumentów na stronie

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

#utworzenie nowego folderu na pobrane szczegóły oferty
docs_folder_name = Path("folder_z_dokumentami_oferty_11111") #zmienić do elastycznej aktualizacji
print(f"ścieżka current name: {docs_folder_name}")
#current_offer_path = Path.cwd()
#print(f"folder w którym zapisana jest oferta numer [dodać automatyczny numer oferty]: {current_offer_path}")

# Sprawdź czy folder istnieje, jeśli nie to utwórz
if not os.path.exists(docs_folder_name):
    docs_folder_name.mkdir()
    print(f"tworzenie folderu na pobrane szczegóły oferty: {docs_folder_name}")
else:
    print(f"Folder o nazwie {docs_folder_name} już istnieje!")


#pobranie dokumentów pdf i zapisanie ich do nowego folderu z tytułem z numerem zapytania i datą pojawienia się zapytania (numer oferty jest automatycznie dołączany przez stronę przy pobieraniu, nie trzeba go zaciągać z danych ani nadawać)




# Zakładamy, że masz już kod do pobierania folderu, a jego ścieżka znajduje się w zmiennej `sciezka_pobranego_folderu`

# Przykładowa ścieżka, gdzie chcesz przenieść pobrany folder
folder_docelowy = docs_folder_name


#znajdywanie nazwy ostatniego pobranego folderu, a nie pliku (ze strony pobierany jest folder z plikami a nie plik)
list_of_zips_in_downloads = [dlded_folder.path for dlded_folder in os.scandir(str(Downloads_dir)) if zipfile.is_zipfile(dlded_folder)] #zebranie tylko folderów, a nie plików, z Pobranych
latest_folder = max(list_of_zips_in_downloads, key=os.path.getctime) #namierzenie ostatniego pobranego folderu - nasz folder z dokumentami
print(f"lista wszystkich znalezionych folderów zip: {list_of_zips_in_downloads}")
print(f"ostatni pobrany folder: {latest_folder}")



# Pełna ścieżka do folderu docelowego
print(f"Ścieżka folderu docelowego: {docs_folder_name}")

# Przeniesienie folderu
shutil.move(latest_folder, docs_folder_name)

print(f'Pobrany folder "{latest_folder}" został przeniesiony do "{docs_folder_name}"')



czekaj2 = input()