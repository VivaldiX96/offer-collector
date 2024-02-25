
# !!! Installed packages (install them in the container - the same set is in the requirements.txt file):
    # pip install selenium==4.16.0
    # https://googlechromelabs.github.io/chrome-for-testing/ - https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/win64/chromedriver-win64.zip
    # pip install openpyxl==3.1.2
    
    # node-v20.10.0-x64
    # pip install --upgrade pymupdf - for text recognition in pdf's 
    # pip install PyMuPDF==1.23.9 - libraries for PDF's reading by the program; >>> in the .py code modules - "import fitz" (this imports the pymupdf library) 
    # pip install openai==0.28.0 - for communication with ChatGPT 
    # pip install streamlit==1.30.0 - for creating the UI with the option of custom instruction for the AI Assistant  
    # pip install googletrans==4.0.0rc1 - for translations of documents' texts from source language to English to supply the text to interpret by LLAMA2 in the module LLAMA2_query_generator.py 
    # pip install replicate==0.23.1 - for interactions with AI from the program instead of hand typing 
    # pip install requests==2.31.0
    # pip install docker==7.0.0 - a library to connect with docker like with docker commands, needed to send queries to an app in a container and reading answers from it (a dockerized LLM model for example)
    # pip install operagxdriver==0.10
    # https://github.com/docker/docker-py
    
    # Libraries that are not used yet - consider installing for adding extra functionalities:
    # pip install beautifulsoup4 - not used, for now selenium is sufficient for the webscraping purposes
    # pip install pydocker - another way to connect with AI in a container
    # pip install pillow - to detect images and text in the images, for example to read any scanned documents
    # pip install python-docx - a library to save documents with a desired style or formatting
    # pip install pyttsx3 - for speech recognition
    # pip install SpeechRecognition - -||-


On installation of the openai package without specifying it's version (using only "pip install openai"), an error can appear:

"Exception has occurred: APIRemovedInV1


You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28` - and after choosing the old version to install, the package should work.

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742"

http://host.docker.internal:11434/api - API address for llama2:3.6 GB