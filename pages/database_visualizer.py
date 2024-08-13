#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 12:15:38 2024

@author: maximeb
"""

import streamlit as st
import pandas as pd
from database_functions import *

    # variables

df = pd.read_csv('database.csv', index_col=0)

    # page layout

st.title('Ontology Database Manager')

st.metric(label='Total Number of Ontology:', value=len(df))

    # database df visualizer

st.header('Ontology Database Viewer')

st.dataframe(df, use_container_width=True)

    # ontology remover

st.header('Remove an Ontology')

        # check if index is an int
    
try:
    index_number = int(st.text_input('Ontology Index Number'))
except:
    st.write('Not a number.')
    
        # remove an ontology
    
remove = st.button('Remove')
    
if remove:
    try:
        remove_ontology(df, index_number)
        st.write("Ontology removed.")
    except:
        st.write("Ontology not found.")