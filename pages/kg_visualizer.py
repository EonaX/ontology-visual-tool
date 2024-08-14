#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 17:29:49 2024

@author: maximeb
"""

import streamlit as st
from gui_functions import *
from graph_functions import *
from rdflib import Graph, Namespace

set_page_config(layout="wide")

st.title('Graph Visualizer')

update_graph_button = st.button('Update Knowledge Graph')
update_viz_button = st.button('Update Visualization')

if update_graph_button:
    
    import ontology_parser
    import kg_constructor

    g = Graph()
    EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
    g.bind("eona", EONA)
    g.parse("data/kg.ttl", format="ttl")
    
    g = filter_graph(g, NAMESPACE=EONA, option='imports')
    draw_graph(g)

if update_viz_button:

    g = Graph()
    EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
    g.bind("eona", EONA)
    g.parse("data/kg.ttl", format="ttl")
    
    g = filter_graph(g, NAMESPACE=EONA, option='imports')
    draw_graph(g)

st.image('data/kg.svg', width=1080)

