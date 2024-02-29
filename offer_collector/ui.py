# this is a small web UI for initializing the main.py in one of 3 possible modes, chosen by the User. 
# temporary - before the other initialization modes are developed, 
# in order to run in the default mode type this phrase in the terminal: "python -m streamlit run Initial_interface.py"

import streamlit as st
import time

#Message "Assistant has been activated" in the title
st.title("Asystent ofertowy został uruchomiony")

#initial setting of the textarea - it changes when the user switches radio buttons to 'Custom command' mode
textarea_disabled = True

radio_button_captions = ['przeszukiwanie ofert z wykrywaniem informacji o wadium i wymaganiach',
                        'wykonanie streszczenia oferty w paru zdaniach',
                        'wprowadź polecenie dla asystenta (np. jakie informacje powinien znaleźć)']

# the titles on radio buttons: 'Default mode', 'Summary', 'Custom command'
radio_button_options = ['Tryb domyślny', 'Streszczenie', 'Dostosowane polecenie']

# The default mode of assistant's operation under index=0 is the first option - to filter the offers based on the info on the initial deposit and requirements that the contractor  has to fullfill
welcome_page = st.radio('Wybierz tryb działania asystenta.' ,
                options = radio_button_options,
                captions = radio_button_captions,  index=0) 

# function to be developed that lets the User choose one of 3 modes of the main program's execution
def assistantModeInitialization():
    match welcome_page:
        case 'Tryb domyślny':
            textarea_disabled = True
            pass
        case 'Streszczenie':
            textarea_disabled = True
            pass
        case 'Dostosowane polecenie':
            textarea_disabled = False
            pass
        #case _:  # "_" means a default mode if no other option was chosen before
            #default_action()  #maybe a default command could be added here later
        
    
# Creating a textfield - initially disabled with the variable "textarea_disabled"
instr_option_field = st.text_area(label='Pusty opis', label_visibility="collapsed", placeholder='Wpisz instrukcję dla Asystenta', disabled=textarea_disabled)

