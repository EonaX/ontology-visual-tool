#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 12:03:46 2024

@author: maximeb
"""

import streamlit as st
from database_functions import *
from gui_functions import *
import pandas as pd
import json
import datetime

set_page_config()

st.title('Ontology Database Manager')

st.header('Ontology Submission Form')

    # load the database

df = pd.read_csv('data/database.csv', index_col=0)

with open('data/ontology.schema', 'r') as f:
    json_schema = json.loads(f.read())

    # submission process

form = st.form(key='my-form', clear_on_submit=True)
name = form.text_input('Name')
provider = form.text_input('Provider')
domain = form.selectbox('Domain',
                        options = json_schema['fields'][2]['enumerate'])
base_uri = form.text_input('Base URI')
download_url = form.text_input('Download URL')
syntax = form.selectbox('Serialization',
                        options = json_schema['fields'][6]['enumerate']
                        )
submit = form.form_submit_button('Submit')

    # add a row to the df

if submit:
    
    today = str(datetime.date.today())
    
    list_of_properties = [name, provider, domain, base_uri, download_url, syntax, today]
    
    error_message = add_ontology(df, list_of_properties)
    
    if error_message:
        st.write(error_message)
    else:
        st.write("Ontology submitted.")