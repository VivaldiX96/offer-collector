
# PLAN NA PROGRAM DLA STRONY https://connect.orlen.pl/servlet/HomeServlet:

    # klikacz przycisku "Pokaż więcej" - na początku 5 razy a nie do końca listy ✓
    # tworzenie listy wszystkich ofert i wrzucanie jej do csv - CsvNaOferty.py
        # włączenie filtru kategorii na stronie aby widać było mniej niepotrzebnych ofert do analizy
    # wejście na stronę dedykowaną pojedynczej ofercie - ReadOffer.py
        # sczytanie danych pojedynczej oferty
        # podzielenie tych danych na kategorie

        # odfiltrowanie ofert oczywistych na podstawie nagłówków (dla późniejszego 
        # / zmniejszenia liczby zapytań do czatu GPT) - CsvNaOferty.py (dodatkowa funkcjonalność)

    # ustawienie chatowi GPT stałych kryteriów oceny i stałego polecenia zwracania 0 lub 1 - ChatEvaluation.py
    # wysłanie danych z jednej oferty do Chatu GPT - zbieracz ofert .py (główny program)
    # wrzucanie ofert oznaczonych przez chat jako "1" do katalogu ofert do rozpatrzenia

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# import webscraper

#dodane opcje w celu niezamykania przeglądarki - na razie niekoniecznie działają
#options = webdriver.ChromeOptions()
#options.add_experimental_option("detach", True)

# Inicjalizacja przeglądarki (w tym przypadku Google Chrome)
driver = webdriver.Chrome()

# Przechodzimy na stronę, która zawiera listę ofert - tutaj strona Orlenu
driver.get('https://connect.orlen.pl/servlet/HomeServlet')


# Ustawiamy maksymalny czas oczekiwania na znalezienie elementu (np. przycisku "Pokaż więcej")
wait = WebDriverWait(driver, 10)

# Pętla do klikania przycisku "Pokaż więcej" dopóki jest dostępny
# while True: #POCZĄTEK KOMENTARZA na pętlę rozwijającą całą listę
#     try:
#         # Znajdujemy przycisk "Pokaż więcej" używając XPath lub innego selektora
#         show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, 'xpath_do_przycisku')))
        
#         # Klikamy przycisk "Pokaż więcej"
#         show_more_button.click()

#         # Tutaj możesz dodać kod do sczytywania kolejnych elementów z listy na stronie
#         # np. elementy = driver.find_elements(By.XPATH, 'xpath_do_elementow')

#     except:
#         # Jeśli nie ma już przycisku "Pokaż więcej", przerywamy pętlę
#         break

# # Zamykamy przeglądarkę po zakończeniu   #KONIEC KOMENTARZA na pętlę rozwijającą całą listę
# driver.quit()

def orlen_expandclicker():
    for licznik in range(1, 6):  # wersja testowa - z 5-krotnym kliknięciem przycisku
        show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "link-btn") and contains(@class, "link-load-more")]')))
        show_more_button.click()
        time.sleep(3)

orlen_expandclicker()


# webscraper()
from bs4 import BeautifulSoup 
import requests 
import csv

driver.get("https://connect.orlen.pl/servlet/HomeServlet") 

# Pobranie widocznej treści z przeglądarki
page = driver.page_source

import pandas as pd
 
oferty = driver.find_elements(By.CLASS_NAME, 'demand-item')

print(f"Liczba ofert: {len(oferty)}")

tabela_ofert = []

for oferta in oferty:
    
    numer_oferty = oferta.find_element(By.CLASS_NAME, 'demand-item-details-number').text
    tytul_oferty = oferta.find_element(By.CLASS_NAME, 'demand-item-details-name').text
    kategoria_oferty = oferta.find_element(By.CLASS_NAME, 'demand-item-details-category').text
    link_do_szczegolow = oferta.find_element(By.CLASS_NAME, 'demand-item-to-details').get_attribute("href") #sprawdzić
    pozostaly_czas = oferta.find_element(By.CLASS_NAME, 'demand-item-time').text
     
    obiekt_ofertowy = {
        'numer': numer_oferty,
        'tytul': tytul_oferty,
        'kategoria': kategoria_oferty,
        'link': link_do_szczegolow,
        'pozostaly czas': pozostaly_czas
    }
    tabela_ofert.append(obiekt_ofertowy)

Orlen_df = pd.DataFrame(tabela_ofert)
print(Orlen_df)

#Orlen_df_csv = Orlen_df.to_csv("tabela ofert.csv")

import os

# nazwa nowego folderu na csv
folder_path = 'folder_na_csv'

# Sprawdź czy folder istnieje, jeśli nie to utwórz
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Ścieżka do pliku CSV w nowo utworzonym folderze
file_path = os.path.join(folder_path, 'tabela_ofert.csv')
print(f"ścieżka pliku: {file_path}")

# Zapisz listę do pliku CSV
#Orlen_df.to_csv(file_path, index=False)
Orlen_df.to_csv(file_path, mode='w', encoding='utf-8-sig', index=False)

""" with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in tabela_ofert:
        csvwriter.writerow([row]) """

print(f"Plik CSV został utworzony w folderze {folder_path}")

#soup = BeautifulSoup (html, "html.parser") 

#url = 'https://connect.orlen.pl/servlet/HomeServlet'

#page = requests.get(url)


# # # tworzenie listy wszystkich ofert i wrzucanie jej do csv - CsvNaOferty.py
# # # PotencjalneProj = CsvNaOferty(html)




# ... kod wczytywania i przetwarzania danych ...
""" 
# Ścieżka do nowo utworzonego folderu
folder_path = 'folder_na_csv'

# Sprawdź czy folder istnieje, jeśli nie to utwórz
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Ścieżka do pliku CSV w nowo utworzonym folderze
file_path = os.path.join(folder_path, 'dane_ofertowe.csv')

# Zapisz listę do pliku CSV
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in Orlen_df:
        csvwriter.writerow([row])

print(f"Plik CSV został utworzony w folderze {folder_path}")
 """
czekaj = input() #dodatkowy dummy task do oczekiwania bez zamykania przeglądarki

# Ustawienie opcji zamykania okna na False
# driver.close()  # nie zamknie okna

# Zamykamy przeglądarkę po zakończeniu
#---dla testu nie zamykamy przeglądarki aby sprawdzić czy lista się rozwija--- driver.quit()





###from bs4 import BeautifulSoup 
###import requests 
###import csv
