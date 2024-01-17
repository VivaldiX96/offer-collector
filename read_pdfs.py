# moduł do czytania pdf - ma wykrywać najpierw, które pdfy zawierają tekst, a które nie, i poddać analizie tekstowej te, które mają tylko grafikę rastrową
# ma przecytane pdfy zwracać w postaci obiektów tekstowych

#biblioteki do czytania pdf: w Powershell - pip install PyMuPDF >>> w kodzie - import fitz # imports the pymupdf library
# pip install pillow - wykrywanie obrazówi tekstu w obrazach
#biblioteki do zapisywania dokumentów z formatowaniem - pip install python-docx

from pathlib import Path
import os
import io
import zipfile
import fitz # PyMuPDF, program do czytania tekstu z pdf-ów

#import summarizer

def read_pdf_files_text():
    print(f"uruchamiam moduł {__name__}")

    #upewnienie sie że moduł działa w folderze utworzonym dla plików które mają być odczytane
    #os.chdir(str(summarizer.docs_folder_name)) 

    # Pobranie listy plików i katalogów w bieżącym folderze
    fold_contents = os.scandir(os.getcwd())

        # Wyłuskanie nazwy pierwszego folderu z rozszerzeniem ".zip" (jeśli istnieje) i wyświetlenie jej; 
        # Pętla przeszukuje po kolei zawartość aż trafi na plik zip
    for file in fold_contents:
        if file.is_file() and file.name.endswith('.zip'):
            zip_file_name = file.name
            zip_file_path = file.path
            print(f"Znaleziono plik zip o nazwie: \"{zip_file_name}\" - czytam tekst zawartych dokumentów...") 
            # Otwarcie pliku ZIP
            with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                # Przejście przez wszystkie pliki w archiwum ZIP
                for file_info in zip_file.infolist():
                    # Sprawdzenie czy plik jest PDF
                    if file_info.filename.endswith(".pdf"):
                        # Otwarcie pliku PDF bez wypakowywania
                        with zip_file.open(file_info) as pdf_file:
                            # Odczyt danych z pliku PDF
                            pdf_data = io.BytesIO(pdf_file.read())
                            # Ekstrakcja tekstu z pliku PDF
                            doc = fitz.open("pdf", pdf_data)
                            text = ""
                            for page_number in range(doc.page_count):
                                page = doc.load_page(page_number)
                                text += page.get_text("text")
                            print("Tekst z pliku PDF:", text)
            break  # Przerwij pętlę po znalezieniu pierwszego pasującego pliku zip 
        #!!zmienić - znajdować wszystkie zipy

# pdf = fitz.open(zip_file_path)


