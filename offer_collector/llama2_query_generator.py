
from googletrans import Translator
import time
import os
import docker


### move this part to the main module later, so that the key is imported only once for the whole program's operation
REPLICATE_API_TOKEN = os.environ["REPLICATE_API_TOKEN"] 
print(REPLICATE_API_TOKEN)
###



## --PROMPTS--
def send_prompt():
    pre_prompt = "You are a helpful assistant. You don't respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    prompt_input = (f"In the text enclosed in triple quotation marks, find important information that provides the answers to the two questions below:
    1. Does the Contractor have to provide any deposit before completing the Employer's order? Answer \"yes\" or \"no\".
    2. Does the Contractor need to have additional qualifications or past experience in performing assignments or contracts similar to those discussed in this document? Answer \"yes\" or \"no\".\n\nProvide your answer in two lines corresponding to the above questions, with each line containing only the number 0 if the answer to the first question is \"no\" or the number 1 if the answer is \"yes\". Write the answers in a format like so:
    Question 1 - [answer]
    Question 2 - [answer]
    where square brackets contain only 'yes' or 'no'.
    Below is the text in triple quotation marks in which you have to find the answers:\n\n{fragment}")




#import read_pdfs   # the texts to translate will be imported from that module, for now I am using the single text in 'AI_test_doc_no_instruction.txt'

pyfile_dir = os.path.dirname(__file__)




##  alternative way of reading the API key - change to this one on target implementation ##
#from OffersCollector
#  import REPLICATE_API_TOKEN
#REPLICATE_API_TOKEN = OffersCollector.REPLICATE_API_TOKEN
## uncomment after taking the part from triple hashtags to the main pyfile  ##

with open('AI_test_doc_no_instruction.txt', 'r', encoding='utf-8-sig') as plik: # A testing rreading of a hand-supplied txt doc   
    doc_text = plik.read()

        # print(f"taki tekst widzi program: {doc_text}") # Checked, the program sees the whole text 

#doc_text = read_pdfs.text_for_AI_to_read # get the function's output from read_pdfs.py - add this doc to the final query sent to LLM



# Separating the text into shorter fragments including the end of a paragraph 
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


#These 2 lines are a temporary code to check the result of the text fragmentation
for index , fragment in enumerate(fragmented_doc_pl):
    print(f"fragment numer {index} w zestawie fragmented_doc_pl:\n{fragment}")

# for fragment in fragmented_doc_pl:
#    print(fragment) 

# Initializing the translator 
translator = Translator()

# Translated each fragment from source language (Polish) to English 
translated_fragments = []
for fragment in fragmented_doc_pl:
    translated_fragment = translator.translate(fragment, src='pl', dest='en').text.replace("\n", " ")
    translated_fragments.append(translated_fragment)
    time.sleep(1) # delay to reduce the risk of blocking Google Translator because of too frequent queries 




# CHECK - result as an array
for index , fragment in enumerate(translated_fragments):
    print(f"fragment numer {index} w zestawie fragmented_doc_pl:\n{fragment}(długość: {len(fragment)} znaków)")


import re

# String with the answer from the LLM 
text_of_AI_answer = "The answer to Question 1 is \"yes\", and the answer to Question 2 is \"no\"."

# Regexes to detect a "yes" or "no" answer in the LLM's response
pattern = r'\"(yes|no)\"'

# Searching for the answers in the text of the LLM's response
answers = re.findall(pattern, text_of_AI_answer)

# Assigning the answers to variables 
ans_for_question_1 = answers[0]
ans_for_question_2 = answers[1]

# Displaying the outcome of LLM's judgement
print("Odpowiedź na pytanie 1:", ans_for_question_1)
print("Odpowiedź na pytanie 2:", ans_for_question_2)