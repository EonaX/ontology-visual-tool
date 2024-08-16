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

set_page_config(layout="wide")

st.title('Graph Visualizer')

    
import ontology_parser
import kg_constructor

# Initializing



default_query = r"""CONSTRUCT {
?provname eona:imports ?provnameImports.
}    

WHERE {
?s a eona:Ontology;
eona:isProvidedBy ?prov;
eona:isNamed ?name;
eona:imports ?imports. 

?imports eona:isNamed ?nameImports;
eona:isProvidedBy ?provImports.

# exclude reflexive triples:
FILTER(!(?s = ?imports)) 

# exclude standard imports:
FILTER( ! (?imports = <http://www.w3.org/2002/07/owl>) )
FILTER( ! (?imports =<http://www.w3.org/2001/XMLSchema>) )
FILTER( ! (?imports =<http://www.w3.org/XML/1998/namespace>) )
FILTER( ! (?imports =<http://www.w3.org/2000/01/rdf-schema>) )
FILTER( ! (?imports =<http://www.w3.org/1999/02/22-rdf-syntax-ns>) )

# concat provider and name of the ontology
BIND(CONCAT(?prov, '\n', ?name) AS ?provname )
BIND(CONCAT(?provImports, '\n', ?nameImports) AS ?provnameImports )
       }"""

query = st.text_area(label='SPARQL Query', value = default_query, height = 160)

launch_query = st.button('Query')

if launch_query:
    
    g = Graph()
    EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
    g.bind("eona", EONA)
    g.parse("data/kg.ttl", format="ttl")
    
    EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
    g.bind("eona", EONA)
    g.parse("data/kg.ttl", format="ttl")
    
    g2 = g.query(query, initNs = {'eona':EONA, 'rdf':RDF})

    g3=Graph()
    
    for s, p, o in g2:
        g3.add((s, p, o))


    # subgraph += g.triples((None, EONA['isNamed'], None))


# forbidden_uris = st.checkbox('Remove forbidden URIs', value=True)
# if forbidden_uris:
#     g3 = remove_forbidden_uris(g3)

# reflexive_triples = st.checkbox('Remove reflexive triples', value=True)
# if reflexive_triples:
#     g3 = remove_reflexive_triples(g3)

# only_imports = st.checkbox('Show only imports triples', value=True)
# if only_imports:
#     g3 = filter_graph(g3, triple = (None, EONA['imports'], None))

# layout_radio = st.radio('Layout', ['spring', 'circular'])
# layout = layout_radio

# Drawing
    subgraph = convert_to_nx(g3)
    nx_graph = draw_graph(subgraph) 

    st.write(len(g3))

st.image('data/kg.svg', width=1080)


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
