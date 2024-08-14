#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 12:15:38 2024

@author: maximeb
"""

import streamlit as st
import pandas as pd
from database_functions import *
from gui_functions import *

set_page_config()

    # variables

df = pd.read_csv('data/database.csv', index_col=0)

    # page layout

st.title('Ontology Database Manager')


    # database df visualizer

st.header('Ontology Database Viewer')

st.dataframe(df, use_container_width=True, 
             column_order=["provider", "name", "domain", "base_uri", "download_url", "syntax", "added_when"],
             column_config={
                 "_index":"ID",
                 "name":"Name",
                 "provider":"Provider",
                 "domain":"Domain",
                 "base_uri":"Base URI",
                 "download_url":"Download URL",
                 "syntax":"Serialization",
                 "added_when":"Added On"
                 })

    # dash board

col1, col2 = st.columns([6,2])

with col1:
    
        # bar graph
    
    bar_graph = count_line_graph(df)
    st.plotly_chart(bar_graph, use_container_width=True)

with col2:
    
        # count metric
    
    ontology_count = ontology_count_metric(df)
    st.plotly_chart(ontology_count, use_container_width=True)

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