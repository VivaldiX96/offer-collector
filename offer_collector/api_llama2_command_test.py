from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initializing the Chrome browser 
driver = webdriver.Chrome()

# Entering the address where Ollama's UI will be displayed to the user

driver.get('localhost:3000')


# Setting max awaiting time for the driver to detect the expected elements
wait = WebDriverWait(driver, 10)

def ollamaInputQuery():
    New_chat_button = wait.until(EC.element_to_be_clickable((By.ID, 'sidebar-new-chat-button')))
    New_chat_button.click()
    time.sleep(3)

ollamaInputQuery()

## expand the module later for web-driver-based contact with the Llama Model