

from bs4 import BeautifulSoup 
import requests 
import csv

page_to_scrape = requests.get("https://connect.orlen.pl/servlet/HomeServlet") 
soup = BeautifulSoup (page_to_scrape.text, "html.parser") 

# Znajdź wszystkie elementy o klasie "demand item", które zawierają tekst "P - wykonanie projektów"
okienka = soup.find_all(class_="demand item", string="P - wykonanie projektów")

# Utwórz listę zawierającą treści znalezionych okienek
tresci_okienek = [okienko.get_text() for okienko in okienka]

# Wyświetl listę zawierającą treści okienek
print(tresci_okienek)

## quotes = soup.findAll("span", attrs={"class":"text"})
## authors = soup.findAll("small", attrs={"class": "author"})


file = open("dane_ofertowe.csv", "w") 
potencjalneOferty = csv.writer(file)

import os

# ... kod wczytywania i przetwarzania danych ...

# Ścieżka do nowo utworzonego folderu
folder_path = 'folder_na_csv'

# Sprawdź czy folder istnieje, jeśli nie to utwórz
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Ścieżka do pliku CSV w nowo utworzonym folderze
file_path = os.path.join(folder_path, 'nazwa_pliku.csv')

# Zapisz listę do pliku CSV
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in tresci_okienek:
        csvwriter.writerow([row])

print(f"Plik CSV został utworzony w folderze {folder_path}")

#potencjalneOferty.writerow(["QUOTES", "AUTHORS"])

#for quote, author in zip (quotes, authors): 
#    print(quote.text+ " " + author.text) 
#    potencjalneOferty.writerow( [quote.text, author.text])
#file.close()