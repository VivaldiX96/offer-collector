
#from googletrans import Translator
import time
import os

with open('Replicate_API_token.txt') as ReplicateAPItoken_textfile:
    ReplicateAPItoken = ReplicateAPItoken_textfile.read()

print(f"Klucz API do replicate: {ReplicateAPItoken}")
#ReplicateAPItoken = os.environ["REPLICATE_API_TOKEN"]

import replicate
#from zbieracz_ofert import Replicate_API_token





#import read_pdfs # z tego modułu będą zaciągane teksty do przetłumaczenia, na razie używam pojedynczego tekstu 'AI_test_doc_no_instruction.txt'

### tą część kodu przenieść później do modułu głównego, aby klucz był zaciągany tylko raz na całe działanie programu
pyfile_dir = os.path.dirname(__file__)

#ReplicateAPItoken = open(ReplicateAPItoken_filepath, mode="r")


###

##  alternatywny sposób zaczytania klucza API - zmienić na ten docelowo   ##
#ReplicateAPItoken = zbieracz_ofert.Replicate_API_token
##  odkomentować po przeniesieniu części z ### do głównego pliku pyfile   ##

""" with open('AI_test_doc_no_instruction.txt', 'r', encoding='utf-8-sig') as plik: #testowe czytanie jednego podłożonego dokumentu txt
    doc_text = plik.read()

        # print(f"taki tekst widzi program: {doc_text}") #sprawdzone, program widzi cały tekst

#doc_text = read_pdfs.text_for_AI_to_read #zaciągnąć wynik funkcji z programu read_pdfs - do dołączenia do ostatecznego query



# Podział tekstu na krótsze fragmenty z uwzględnieniem zakończenia akapitu
def Split_into_fragments(doc_text, max_length=3900):
    fragmented = []
    while doc_text:
        if len(doc_text) <= max_length:
            fragmented.append(doc_text)
            break
        else:
            separation = max_length
            while doc_text[separation] != '.':
                separation -= 1
            fragmented.append(doc_text[:separation+1])
            doc_text = doc_text[separation+1:].lstrip()
    return fragmented


fragmented_doc_pl = Split_into_fragments(doc_text)

for index , fragment in enumerate(fragmented_doc_pl):
    print(f"fragment numer {index} w zestawie fragmented_doc_pl:\n{fragment}")

# for fragment in fragmented_doc_pl:
#    print(fragment) 

# Inicjalizacja translatora
translator = Translator()

# Przetłumaczenie fragmentów z polskiego na angielski
translated_fragments = []
for fragment in fragmented_doc_pl:
    translated_fragment = translator.translate(fragment, src='pl', dest='en').text.replace("\n", " ")
    translated_fragments.append(translated_fragment)
    time.sleep(1) #opóźnienie aby nie zadawać zapytań z maksymalną częstotliwością by zmniejszyć ryzyko zablokowania serwisu




# DO SPRAWDZENIA - Wynik w postaci obiektu typu array
for index , fragment in enumerate(translated_fragments):
    print(f"fragment numer {index} w zestawie fragmented_doc_pl:\n{fragment}(długość: {len(fragment)} znaków)")


import re

# Tekst z odpowiedzią modelu
tekst_odpowiedzi = "The answer to Question 1 is \"yes\", and the answer to Question 2 is \"no\"."

# Wyrażenia regularne do wykrycia odpowiedzi "yes" albo "no"
pattern = r'\"(yes|no)\"'

# Wyszukiwanie odpowiedzi w tekście
odpowiedzi = re.findall(pattern, tekst_odpowiedzi)

# Przyporządkowanie odpowiedzi do zmiennych
odpowiedz_pytanie_1 = odpowiedzi[0]
odpowiedz_pytanie_2 = odpowiedzi[1]

# Wyświetlenie wyników
print("Odpowiedź na pytanie 1:", odpowiedz_pytanie_1)
print("Odpowiedź na pytanie 2:", odpowiedz_pytanie_2) """