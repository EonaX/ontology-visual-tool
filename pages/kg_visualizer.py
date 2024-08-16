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

    
import ontology_parser
import kg_constructor

# Initializing

g = Graph()
EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
g.bind("eona", EONA)
g.parse("data/kg.ttl", format="ttl")

# Cleaning

forbidden_uris = st.checkbox('Remove forbidden URIs', value=True)
if forbidden_uris:
    g = remove_forbidden_uris(g)

reflexive_triples = st.checkbox('Remove reflexive triples', value=True)
if reflexive_triples:
    g = remove_reflexive_triples(g)

only_imports = st.checkbox('Show only imports triples', value=True)
if only_imports:
    g = filter_graph(g, triple = (None, EONA['imports'], None))

layout_radio = st.radio('Layout', ['spring', 'circular'])
layout = layout_radio
# subgraph += g.triples((None, EONA['isNamed'], None))

# Drawing
subgraph = convert_to_nx(g)
draw_graph(subgraph, layout)

st.image('data/kg.svg', width=1080)

