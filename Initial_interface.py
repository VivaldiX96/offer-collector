# by uruchomić, wpisać w terminalu "python -m streamlit run Initial_interface.py"

import streamlit as st
import time

st.title("Asystent ofertowy został uruchomiony")

textarea_disabled = True

radio_button_captions = ['przeszukiwanie ofert z wykrywaniem informacji o wadium i wymaganiach',
                        'wykonanie streszczenia oferty w paru zdaniach',
                        'wprowadź polecenie dla asystenta (np. jakie informacje powinien znaleźć)']

radio_button_options = ['Tryb domyślny', 'Streszczenie', 'Dostosowane polecenie']


#domyślne ustawienie działania pod index=0 to pierwsza opcja - odsianie ofert na podstawie informacji o wadium i warunkach do spełnienia
page = st.radio('Wybierz tryb działania asystenta.' ,
                options = radio_button_options,
                captions = radio_button_captions,  index=0) 


#def assistant_mode_initialization():
match page:
    case 'Tryb domyślny':
        textarea_disabled = True
        pass
    case 'Streszczenie':
        textarea_disabled = True
        pass
    case 'Dostosowane polecenie':
        textarea_disabled = False
        pass
    #case _:  # "_" oznacza tryb domyślny, jeśli żadna inna opcja nie była wcześniej wybrana
        #default_action()  #być może warto będzie dopisać domyślne polecenie w tym miejscu

# Utworzenie pola tekstowego z uwzględnieniem zmiennej textarea_disabled
instr_option_field = st.text_area(label='Pusty opis', label_visibility="collapsed", placeholder='Wpisz instrukcję dla Asystenta', disabled=textarea_disabled)

