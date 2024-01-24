
import openai
import os
#import streamlit

import

import read_pdfs

text = read_pdfs.text_for_AI_to_read #zaciągnąć wynik funkcji z programu read_pdfs - do dołączenia do ostatecznego query


#driver = webdriver.Chrome(options=options)

# Przekazanie tekstu zapytania do AI 
query = text

system_instructions = "Jesteś wirtualnym asystentem przeszukującym tekst zamówienia w celu znalezienia informacji o tym, czy od wykonawcy projektu wymagane jest wniesienie zabezpieczenia (inne możliwe określenia to \"wadium\" lub \"zastaw\"). Masz także sprawdzać, czy w podanym tekście jest mowa o dodatkowych wymaganiach od wykonawcy, na przykład czy potrzeba specjalnych uprawnień albo okreslonych projektów wykonanych w przeszłości przez wykonawcę."

parameters = {
  'model': 'gpt-3.5.turbo', 
  'messages': [{"role": "system", "content": system_instructions}, 
               {"role": "user", "content": query}, 
               {"role": "assistant", "content": ...}] # poprawić kod aby parametry asystenta, systemu i użytkownika dało się wczytać razem
}

openai.api_key = os.getenv("OPENAI_API_KEY")


completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": system_instructions}
{"role": "user", "content": query}
                                                                           ])
print(completion.choices[0].message.content)




czekaj3 = input()

