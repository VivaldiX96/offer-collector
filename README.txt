
# !!! Installed packages (install them in the container - the same set is in the requirements.txt file):





    
     Libraries that are not used yet - consider installing for adding extra functionalities:
     pip install beautifulsoup4 - not used, for now selenium is sufficient for the webscraping purposes
     pip install pydocker - another way to connect with AI in a container
     pip install pillow - to detect images and text in the images, for example to read any scanned documents
     pip install python-docx - a library to save documents with a desired style or formatting
     pip install pyttsx3 - for speech recognition
     pip install SpeechRecognition - -||-

In order to run the program to update your Offers Database, run the main .py file. 
NOTE: It is recommended to schedule the run of this program as a daily task, for example using Windows Task Scheduler,
outside the working hours (running the Llama2 language model requires a lot of free system resources to operate, mostly RAM and GPU)


The Replicate token must be generated on the official Replicate's website by the User (an account registration is needed in order
to generate User's personal Replicate API token), and added to the System Variables on User's PC



If you want tot use OpenAI's ChatGPT, you should pin your installation to the old version, e.g. `pip install openai==0.28` - 
- installing of the openai package without specifying it's version (using only "pip install openai"), can result in an exception


http://host.docker.internal:11434/api - API address for llama2:3.6 GB

---FUNCTIONALITIES TO ADD---
    -adding the options: 1. to write a summary of a chosen Offer or 2. to
    -showing a system notification about new preferable offers marked by the assistant (+option to turn on/off)
    -sending a mobile and/or email notification to the User (+option to turn on/off)
    -after an open-source LLM trained on other languages is available, enable direct reading the documents in the original language
     instead of translating to English before sending the input to the LLM - a better assessment accuracy might be achieved that way