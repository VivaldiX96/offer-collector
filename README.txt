
# !!! Installed packages (install them in the container - the same set is in the requirements.txt file):





    
     Libraries that are not used yet - consider installing for adding extra functionalities:
     pip install beautifulsoup4 - not used, for now selenium is sufficient for the webscraping purposes
     pip install pydocker - another way to connect with AI in a container
     pip install pillow - to detect images and text in the images, for example to read any scanned documents
     pip install python-docx - a library to save documents with a desired style or formatting
     pip install pyttsx3 - for speech recognition
     pip install SpeechRecognition - -||-


On installation of the openai package without specifying it's version (using only "pip install openai"), an error can appear:

"Exception has occurred: APIRemovedInV1


You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run `openai migrate` to automatically upgrade your codebase to use the 1.0.0 interface. 

Alternatively, you can pin your installation to the old version, e.g. `pip install openai==0.28` - and after choosing the old version to install, the package should work.

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742"

http://host.docker.internal:11434/api - API address for llama2:3.6 GB