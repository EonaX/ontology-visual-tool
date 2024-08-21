#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:51:17 2024

@author: maximeb
"""

import streamlit as st
from gui_functions import *
from graph_functions import *
from rdflib import Graph, Namespace
from rdflib.namespace import RDF
import streamlit.components.v1 as components
from pyvis.network import Network
import base64
from kg_constructor import construct_kg
from ontology_parser import add_record

# Initializing
set_page_config(layout="wide")


#g = Graph()
#EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
#g.bind("eona", EONA)
#g.parse("data/kg.ttl", format="ttl")

df = add_record()
g = construct_kg(df)
EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
g.bind("eona", EONA)

with open('data/default_sparql_query.ttl', 'r') as f:
    default_query = f.read()

        
query = st.text_area(label='SPARQL Query', value = default_query, height = 160)

#HtmlFile = open('data/mygraph.html', 'r')
#raw_html = HtmlFile.read().encode("utf-8")
#raw_html = base64.b64encode(raw_html).decode()
#components.iframe(f"data:text/html;base64,{raw_html}", height=710)

    
g = g.query(query, initNs = {'eona':EONA, 'rdf':RDF})
   
subgraph = convert_to_nx(g)
size_button = st.button('Sized Nodes')

if size_button:
    subgraph = size_by_degree(subgraph)

net = Network('700px', width="100%", directed=True, bgcolor="#222222", font_color="white") 
net.from_nx(subgraph)
net.save_graph('data/mygraph.html')

HtmlFile = open('data/mygraph.html', 'r')
raw_html = HtmlFile.read().encode("utf-8")
raw_html = base64.b64encode(raw_html).decode()
components.iframe(f"data:text/html;base64,{raw_html}", height=710)
