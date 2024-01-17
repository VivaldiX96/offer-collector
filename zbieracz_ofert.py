
# PLAN NA PROGRAM DLA STRONY https://connect.orlen.pl/servlet/HomeServlet:

    # klikacz przycisku "Pokaż więcej" - na początku 5 razy a nie do końca listy ✓
    # tworzenie listy wszystkich ofert i wrzucanie jej do csv - CsvNaOferty.py
        # opcjonalnie - włączenie filtru kategorii na stronie aby widać było mniej niepotrzebnych ofert do analizy (na razei rozwiązane filtrowaniem zebranych ofert w obiekcie Dataframe)
    # wejście na stronę dedykowaną pojedynczej ofercie - ReadOffer.py
        # pobranie dokumentu (pdf, doc, etc.) ze szczegółowym opisem oferty
        # sczytanie tekstu z dokumentu pojedynczej oferty
        # sprawdzenie obecności wadium lub pokrewnego określenia - można zrobić programem do procesowania mowy
        # wysłanie opisu oferty do AI w celu streszczenia

        # odfiltrowanie ofert oczywistych na podstawie nagłówków (dla późniejszego 
        # / zmniejszenia liczby zapytań do czatu GPT) - CsvNaOferty.py (dodatkowa funkcjonalność)

    # 
    # ustawienie chatowi GPT stałych kryteriów oceny i stałego polecenia zwracania 0 lub 1 - ChatEvaluation.py
    # wysłanie danych z jednej oferty do Chatu GPT - zbieracz ofert .py (główny program)
    # wrzucanie ofert oznaczonych przez chat jako "1" do katalogu ofert do rozpatrzenia

# !!! zainstalowane pakiety (doinstalować na docelowym komputerze przed uruchomieniem programu):
    # pip install selenium
    # https://googlechromelabs.github.io/chrome-for-testing/ - https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/win64/chromedriver-win64.zip
    # pip install openpyxl
    # pip install beautifulsoup4
    # node-v20.10.0-x64
    # pip install --upgrade pymupdf - do rozpoznawania tekstu w pdf-ach
    # pip install PyMuPDF - biblioteki do czytania pdf; w kodzie - import fitz # imports the pymupdf library
    # pip install pillow - wykrywanie obrazówi tekstu w obrazach
    # pip install python-docx - biblioteki do zapisywania dokumentów z formatowaniem - 
    # pip install pyttsx3 - do rozpoznawania mowy
    # pip install SpeechRecognition

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pathlib
import posixpath

# import webscraper # <- zaimportowanie drugiego modułu programu

#dodane opcje w celu niezamykania przeglądarki - na razie niekoniecznie działają
#options = webdriver.ChromeOptions()
#options.add_experimental_option("detach", True)

# Inicjalizacja przeglądarki (w tym przypadku Google Chrome)
driver = webdriver.Chrome()

# Przechodzimy na stronę, która zawiera listę ofert - tutaj strona Orlenu; pobranie widocznej treści z przeglądarki

driver.get('https://connect.orlen.pl/servlet/HomeServlet')


# Ustawiamy maksymalny czas oczekiwania na znalezienie elementu (np. przycisku "Pokaż więcej")
wait = WebDriverWait(driver, 10)

def orlen_expandclicker():
    for licznik in range(1, 6):  # wersja testowa - z 5-krotnym kliknięciem przycisku
        show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "link-btn") and contains(@class, "link-load-more")]')))
        show_more_button.click()
        time.sleep(3)

orlen_expandclicker()


# webscraper() # początek



import pandas as pd
 
oferty = driver.find_elements(By.CLASS_NAME, 'demand-item')

print(f"Liczba ofert: {len(oferty)}")

tabela_ofert = []

for oferta in oferty:
    
    numer_oferty = oferta.find_element(By.CLASS_NAME, 'demand-item-details-number').text
    tytul_oferty = oferta.find_element(By.CLASS_NAME, 'demand-item-details-name').text
    kategoria_oferty = oferta.find_element(By.CLASS_NAME, 'demand-item-details-category').text
    link_do_szczegolow = oferta.find_element(By.CLASS_NAME, 'demand-item-to-details').get_attribute("href")
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

#kod filtrujący obiekty ofertowe po kategorii
Orlen_df = Orlen_df[Orlen_df.kategoria.str.contains('Dokumentacja - projekty techniczne')]
print(f"Liczba ofert z kategorii \"Wykonanie projektów\": {len(Orlen_df.index)}")
print(Orlen_df)


import os

#ustalenie ścieżki, gdzie będzie umieszczony ten plik .py i zmiana ściezki na aktualną
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)



### print(f"ścieżka folderu roboczego: {Path.cwd()}") ### - te dwie linijki można aktywować w celach kontrolnych
### print(f"ścieżka pliku Python: {Path(__file__)}") ### - pozwalają sprawdzić, gdzie jest program i gdzie zapisze pliki

# nazwa nowego folderu na csv
folder_path = 'folder_na_csv'

# Sprawdź czy folder istnieje, jeśli nie to utwórz
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder o nazwie {folder_path} jeszcze nie istnieje w katalogu roboczym; \ntworzenie nowego folderu {folder_path}...")


# Załóżmy, że masz DataFrame o nazwie df i zmienną folder_path zawierającą ścieżkę do folderu
nazwa_pliku_excel = 'Arkusz_ofert.xlsx'
sciezka_do_pliku_excel = os.path.join(folder_path, nazwa_pliku_excel)

# importowanie poprzednio wygenerowanego arkusza, jeśli istnieje
if os.path.isfile(sciezka_do_pliku_excel):
    # Wczytanie pliku Excel do obiektu DataFrame
    Poprzedni_Orlen_df = pd.read_excel(sciezka_do_pliku_excel)
    print("Aktualizacja pliku excel...")

    #### newdf=pd.concat([Poprzedni_Orlen_df, Orlen_df]).drop_duplicates(keep=False) # kod do uzyskania różnicy starego i nowego Df

    # łączenie poprzedniego arkusza z nowym
    Orlen_df_nowe_rzedy = Orlen_df.merge(Poprzedni_Orlen_df, on='numer', how='outer', indicator=True)
    print(f"Nowy arkusz z indykatorami dla sprawdzenia: {Orlen_df_nowe_rzedy}")
    
    # wybierz tylko nowe rzędy
    nowe_rzedy = Orlen_df_nowe_rzedy.query('_merge == "left_only"').drop(columns=['_merge'])

    # wynikowy DataFrame
    print(f"nowe oferty: \n{nowe_rzedy}")

    # nowy Dataframe bez kolumny indicator, który zostanie wyeksportowany do excela:
    Orlen_df = Orlen_df.merge(Poprzedni_Orlen_df, on='numer', how='outer', indicator=False)

    print(f"Nowy plik excel: {Orlen_df}")

else:
    # komunikat o braku poprzedniego arkusza i o lokacji utworzeniu nowego
    print(f"Plik o nazwie {nazwa_pliku_excel} jeszcze nie istnieje w folderze w katalogu roboczym; \ntworzenie nowego pliku w folderze {folder_path}...")


# Teraz możesz zapisać DataFrame do pliku <link>Excel</link> pod wskazaną ścieżką
Orlen_df.to_excel(sciezka_do_pliku_excel, index=False, sheet_name='Wstępne_oferty')
sciezka_do_pliku_excel_abs = os.path.abspath(sciezka_do_pliku_excel)
print(f"Arkusz Excel został utworzony w folderze {folder_path}.\nŚcieżka pliku: {sciezka_do_pliku_excel_abs}")

# Ścieżka do pliku CSV w nowo utworzonym folderze
file_path = os.path.join(folder_path, 'tabela_ofert.csv')
absolute_path = os.path.abspath(file_path)
#print(f"ścieżka pliku: {absolute_path}")

# Zapisz listę do pliku CSV
#Orlen_df.to_csv(file_path, index=False)
Orlen_df.to_csv(file_path, mode='w', encoding='utf-8-sig', index=False) 
print(f"Plik CSV został utworzony w folderze {folder_path}.\nŚcieżka pliku: {absolute_path}")


# Dopisz do istniejącego arkusza Excel
#with pd.ExcelWriter('arkusz_ofert.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:   
    #Orlen_df.to_excel(writer, sheet_name='Wstępne_oferty2') #kod do opracowania by dopisywał linijki na tej samej stronie, a poprzednie przesuwał w dół





# # # tworzenie listy wszystkich ofert i wrzucanie jej do csv - CsvNaOferty.py
# # # PotencjalneProj = CsvNaOferty(html)




# ... kod wczytywania i przetwarzania danych ...

czekaj = input() #dodatkowy dummy task do oczekiwania bez zamykania przeglądarki

# Ustawienie opcji zamykania okna na False
# driver.close()  # nie zamknie okna

