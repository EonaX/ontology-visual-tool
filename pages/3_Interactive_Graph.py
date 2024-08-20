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

# Initializing
set_page_config(layout="wide")

update_kg = st.button('Update')

if update_kg:
    import ontology_parser
    import kg_constructor


g = Graph()
EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
g.bind("eona", EONA)
g.parse("data/kg.ttl", format="ttl")

with open('data/default_sparql_query.ttl', 'r') as f:
    default_query = f.read()

        
query = st.text_area(label='SPARQL Query', value = default_query, height = 160)

launch_query = st.button('Visualize Graph', key='launch_query')

HtmlFile = open('data/mygraph.html', 'r')
raw_html = HtmlFile.read().encode("utf-8")
raw_html = base64.b64encode(raw_html).decode()
components.iframe(f"data:text/html;base64,{raw_html}", height=710)

if launch_query:
    
    g = g.query(query, initNs = {'eona':EONA, 'rdf':RDF})
    
    subgraph = convert_to_nx(g)
    nx_graph = draw_graph(subgraph) 

    net = Network('700px', '1720px', directed=True)
    net.from_nx(subgraph)
    net.save_graph('data/mygraph.html')
