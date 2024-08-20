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
from graph_functions import *
from kg_constructor import set_uris
from rdflib import Graph, Namespace


set_page_config()

# variables

df = pd.read_pickle('data/df.pkl')

# page layout

st.title('Ontology Database Manager')


# database df visualizer

st.header('Ontology Database Viewer')

update = st.button('Update')

if update:
    import ontology_parser

st.dataframe(df, use_container_width=True, 
             column_order=["provider", "name", "domain", "base_uri", "download_url", "syntax", "count_uri", "added_when"],
             column_config={
                 "_index":"ID",
                 "name":"Name",
                 "provider":"Provider",
                 "domain":"Domain",
                 "base_uri":"Base URI",
                 "download_url":"Download URL",
                 "syntax":"Serialization",
                 "count_uri": "Imports Count",
                 "added_when":"Added On"
                 })

# dash board
    
    # bar graph

bar_graph = count_line_graph(df, title = '<b>Ontology Count Over Time</b>')
st.plotly_chart(bar_graph, use_container_width=True)

    # count metrics

col1, col2, col3 = st.columns(3)

with col1:     
    
    ontology_count = ontology_count_metric(df, title = '<b>Total Ontology Count</b>')
    st.plotly_chart(ontology_count, use_container_width=True)

with col2:
    
    ontology_links_count = ontology_count_metric(set_uris, title = '<b>Linked Ontology Count</b>')
    st.plotly_chart(ontology_links_count, use_container_width=True)
    
with col3:
    
    provider_count = ontology_count_metric(df['provider'].unique(), title = '<b>Number of Providers</b>')
    st.plotly_chart(provider_count, use_container_width=True)

# Graph Visualizer

    # Display

st.image('data/kg.svg')

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
