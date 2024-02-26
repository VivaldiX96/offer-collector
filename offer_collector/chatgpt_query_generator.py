
#NOTE: this module is written to test ChatGPT's capability of handling the task. The target solution is to use an open-source LLM so that the whole assistant does not generate extra costs

import os
import openai
#import streamlit  #use it later to extend the functionality and display the ChatGPT's output to the user if necessary

import read_pdfs # module reading texts from the downloaded pdf documents fro each architectural project

text_of_pdfs = read_pdfs.text_for_AI_to_read #pull the function's output from the zaciągnąć wynik funkcji z programu read_pdfs - do dołączenia do ostatecznego query

#driver = webdriver.Chrome(options=options)

# Passing the query to the AI; 
# Query and system instructions are written in Polish since the client is Polish
# This query is sent to ChatGPT that handles Polish; if you want to use an alternative LLM,... 
# ...check if it was trained on Polish language - introduce translating agent if the LLM works only in English
query = text_of_pdfs

# constant initial instructions for ChatGPT in the language of program's user
system_instructions = "Jesteś wirtualnym asystentem przeszukującym tekst zamówienia w celu znalezienia informacji o tym, czy od wykonawcy projektu wymagane jest wniesienie zabezpieczenia (inne możliwe określenia to \"wadium\" lub \"zastaw\"). Masz także sprawdzać, czy w podanym tekście jest mowa o dodatkowych wymaganiach od wykonawcy, na przykład czy potrzeba specjalnych uprawnień albo okreslonych projektów wykonanych w przeszłości przez wykonawcę."

parameters = {
  'model': 'gpt-3.5.turbo', 
  'messages': [{"role": "system", "content": system_instructions}, 
               {"role": "user", "content": query}, 
               {"role": "assistant", "content": None}] # adjust the code later in order to be able to read system's, user's and assistant's parameters together
              
}

# getting the API key for ChatGPT from an environment variable on user's machine
openai.api_key = os.getenv("OPENAI_API_KEY")


completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                          messages=[{"role": "system", "content": system_instructions}, 
                                                    {"role": "user", "content": query}
                                                    ]
                                          )

#printing the ChatGPT's response
print(completion.choices[0].message.content)


