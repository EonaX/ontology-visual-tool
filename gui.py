#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 12:03:46 2024

@author: maximeb
"""

import streamlit as st
from database_functions import *
import pandas as pd

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="centered",
)

st.title('Ontology Database Manager')

st.header('Ontology Submission Form')

    # load the database

df = pd.read_csv('database.csv', index_col=0)

    # submission process

form = st.form(key='my-form', clear_on_submit=True)
name = form.text_input('Name')
provider = form.text_input('Provider')
domain = form.text_input('Domain')
base_uri = form.text_input('Preffered Base URI')
download_url = form.text_input('Latest Version Download URL')
syntax = form.selectbox('Syntax',
                        ('ttl', 'rdf', 'xml')
                        )
submit = form.form_submit_button('Submit')

    # add a row to the df

if submit:
    
    list_of_properties = [name, provider, domain, base_uri, download_url, syntax]
    
    add_ontology(df, list_of_properties)
    
    st.write("Ontology submitted.")