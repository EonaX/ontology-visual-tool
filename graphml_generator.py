#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 17:29:49 2024

@author: maximeb
"""

from ontology_functions import forbidden_uris
from rdflib.extras.external_graph_libs import *
from rdflib import Namespace, Graph, Literal, URIRef
import networkx as nx
import matplotlib.pyplot as plt

kg_ontology = Graph()
EONA = Namespace("http://www.eona-x.eu/ontology/tracking/")
kg_ontology.bind("eona", EONA)
kg_ontology.parse("kg.ttl", format="ttl")


    # subgraph containing only imports

subgraph = Graph()
subgraph.bind("eona", EONA)

# subgraph += kg_ontology.triples((None, RDF.type, None))
subgraph += kg_ontology.triples((None, EONA.imports, None))

for n in forbidden_uris:
    subgraph.remove((None, None, Literal(n)))
    subgraph.remove((None, None, URIRef(n)))



subgraph.serialize(destination='sub_kg.ttl')

nx_graph = rdflib_to_networkx_multidigraph(subgraph)
nx.write_graphml(nx_graph,"sub_kg.graphml")

    #%% drawing

plt.rcParams.update({'text.color': "red",
                     'axes.labelcolor': "green",
                     'lines.color':'green'})

plt.figure(figsize=(19.2,10.8*1.2))
nx.draw_circular(nx_graph, with_labels=True)
plt.tight_layout()
plt.savefig('docs/kg.svg', format='svg', transparent=False)

#%%

