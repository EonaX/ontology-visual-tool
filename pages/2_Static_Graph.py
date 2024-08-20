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
from rdflib.namespace import RDF
from sparql_queries import imports_further, imports_near

set_page_config(layout="wide")

st.title('Graph Visualizer')

    
import ontology_parser
import kg_constructor

# Initializing

g = Graph()
EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
g.bind("eona", EONA)
g.parse("data/kg.ttl", format="ttl")

col1, col2, col3 = st.columns([3, 2, 2])


with open('data/default_sparql_query.ttl', 'r') as f:
    default_query = f.read()

with col1:
        
    query = st.text_area(label='SPARQL Query', value = default_query, height = 160)
    
    cola, colb = st.columns([2, 10])
    
    with cola:
    
        launch_query = st.button('Query', key='launch_query')
        
        if launch_query:
            
            g2 = g.query(query, initNs = {'eona':EONA, 'rdf':RDF})
            
    with colb:
        
        save_query = st.button('Save', key = 'save_query')
        
        if save_query:
            
            with open('data/default_sparql_query.ttl', 'w') as f:
                f.write(query)

with col2:
    imports_further_button = st.button('Imports Further', key='imports_further_button')
    
    if imports_further_button:
        
        query = imports_further
        
        g2 = g.query(query, initNs = {'eona':EONA, 'rdf':RDF})
            
with col3:
    imports_nearer_button = st.button('Imports Nearer', key='imports_nearer_button')
    
    if imports_nearer_button:
        
        query = imports_near
        
        g2 = g.query(query, initNs = {'eona':EONA, 'rdf':RDF})
    
try:
    g3=Graph()
    
    for s, p, o in g2:
        g3.add((s, p, o))
    
    # Drawing
    subgraph = convert_to_nx(g3)
    nx_graph = draw_graph(subgraph) 
    
    st.write('Number of nodes:', nx_graph.number_of_nodes())
    
except:
    pass

st.image('data/kg.png', width=1080)


#%%

# g = Graph()
# EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
# g.bind("eona", EONA)
# g.parse("data/kg.ttl", format="ttl")

# query = """CONSTRUCT {?name1 eona:imports ?name2}    

# WHERE {?s a eona:Ontology;
#         eona:isNamed ?name1;
#         eona:imports ?imports.
       
#         ?imports a eona:Ontology;
#         eona:isNamed ?name2}
#     """
    
# g2 = g.query(query,
#             initNs = {'eona':EONA,
#                       'rdf':RDF})

# g3 =Graph()
# for s, p, o in g2:
#     g3.add((s, p, o))
    
# for s, p, o in g3:
#     print((s, p, o))
