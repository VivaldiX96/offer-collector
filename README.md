I have been creating a virtual assistant that gathers job offers for
architects and then reads, analyzes, and assigns a classification to
the documents tied to each offer to reduce the human workload
required to find new job offers that fulfill the needs of a small
company.

**THE PLAN OF THE PROGRAM WRITTEN FOR GATHERING DATA FROM THE PAGE https://connect.orlen.pl/servlet/HomeServlet:**

     - A clicker of the "Show more" button on the webscraped page  ✓
     - Creating the list of all offers and saving it in a csv file  ✓
        - Optional - enabling the cathegory filter on the website so that less incompatible offers are displayed and delivered to the program for analysis (preliminarily - solved with a filter affecting the Dataframe object of all offers taken from the source website)
     - Entering the sub-website dedicated to a chosen offer  ✓
     - Downloading the documents (pdf, doc, etc.) with a detailed description of a single offer  ✓
     - Reading the text from a single offer  ✓
     - Detecting the keywords from a chosen set in the downloaded documents - could be done with a speech processing program using linguistic functions for more elastic adjustment of the keywords' pool
     - Sending the docs of the offer to LLM (preferably open-source) for summarization
     - Filtering obvious negligible offers based on their titles or cathegories on the website providing the offers for reducing the number of the resulting queries sent to the LLM


     - Setting the constant criterions of assessment for ChatGPT and a constant command to return "0" or "1"  ✓
     - Sending the data from one offer to ChatGPT - main.py
     - Sending offers marked with "1" to the folder of offers to consider for the end user

In order to run the program to update your Offers Database, run the main .py file.
_NOTE: It is recommended to schedule the run of this program as a daily task, for example using Windows Task Scheduler, outside the working hours (running the Llama2 language model requires a lot of free system resources to operate, mostly RAM and GPU)_

The **Replicate token** must be generated on the official Replicate's website by the User (an account registration is needed in order to generate User's personal Replicate API token), and added to the System Variables on User's PC

If you want tot use OpenAI's ChatGPT, you should pin your installation to the old version, e.g. `pip install openai==0.28` -

- installing of the openai package without specifying it's version (using only "pip install openai"), can result in an exception

http://host.docker.internal:11434/api - API address for llama2:3.6 GB

**---FUNCTIONALITIES TO ADD---**

     -adding the options: 1. to write a summary of a chosen Offer or 2. to
     -showing a system notification about new preferable offers marked by the assistant (+option to turn on/off)
     -sending a mobile and/or email notification to the User (+option to turn on/off)
     -after an open-source LLM trained on other languages is available, enable direct reading the documents in   the original language instead of translating to English before sending the input to the LLM - a better assessment accuracy might be achieved that way

_Libraries that are not used yet - consider installing for adding extra functionalities:_
_pip install beautifulsoup4 - not used, for now selenium is sufficient for the webscraping purposes_
_pip install pydocker - another way to connect with AI in a container_
_pip install pillow - to detect images and text in the images, for example to read any scanned documents_
_pip install python-docx - a library to save documents with a desired style or formatting_
_pip install pyttsx3 - for speech recognition_
_pip install SpeechRecognition - -||-_
