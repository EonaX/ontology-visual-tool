#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 17:29:49 2024

@author: maximeb
"""

from ontology_functions import forbidden_uris
from rdflib.extras.external_graph_libs import *
import networkx as nx
import matplotlib.pyplot as plt

graph = Graph()
graph.parse("kg.ttl", format="ttl")

    # subgraph containing only imports

subgraph = Graph()
#subgraph += graph.triples((None, RDF.type, None))
subgraph += graph.triples((None, EONA.imports, None))

for n in forbidden_uris:
    subgraph.remove((None, None, URIRef(n)))

subgraph.serialize(destination='sub_kg.ttl')

nx_graph = rdflib_to_networkx_multidigraph(subgraph)
nx.write_graphml(nx_graph,"sub_kg.graphml")

    #%% drawing

plt.figure(figsize=(19.2*2,10.8*2))
plt.title('KG Imports Graph', fontdict={'size':100})
nx.draw_circular(nx_graph, with_labels=True)
plt.savefig('docs/kg.png')

#%%

