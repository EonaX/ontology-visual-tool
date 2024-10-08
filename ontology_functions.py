#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 18:41:47 2024

@author: maximeb
"""

import requests
from rdflib.extras.external_graph_libs import *
from rdflib import Namespace, Graph, Literal, URIRef
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv

forbidden_uris = ['http://www.w3.org/2002/07/owl', 
                  'http://www.w3.org/1999/02/22-rdf-syntax-ns', 
                  'http://www.w3.org/2000/01/rdf-schema',
                  'http://www.w3.org/XML/1998/namespace',
                  'http://www.w3.org/2001/XMLSchema'
                  ]

# Ontology functions

def extract_imports_ttl(url):
    """
    Extract all base URIS of ontologies imported in Turtle ontology.

    Parameters
    ----------
    url : TYPE
        DESCRIPTION.

    Returns
    -------
    imports_list : TYPE
        DESCRIPTION.

    """
    r = requests.get(url)

    ontology = r.text

    ontology = ontology.split('prefix')[1:]

    imports_list = []

    for n in ontology:
        try:
            
            # check = check_forbidden_uris(n) # not needed since we can do further restrictions afterwards
            
            # if check == True:
                
                n = n.split('<')[1]
                n = n.split('>')[0]
                
                n = remove_suffix(n)
                
                imports_list.append(n)
                
            

        except IndexError:
            pass
            
    return imports_list

def extract_imports_rdf(url="http://xmlns.com/foaf/spec/index.rdf"):
    """
    Extract all base URIS of ontologies imported in a RDF/XML ontology.

    Parameters
    ----------
    url : TYPE, optional
        DESCRIPTION. The default is "http://xmlns.com/foaf/spec/index.rdf".

    Returns
    -------
    imports_list : TYPE
        DESCRIPTION.

    """
    r = requests.get(url)

    ontology = r.text
    
    imports_list = []
          
    try:
        
        # multiple split to isolate base uris
        
        ontology = ontology.split('<rdf:RDF ')[1].split(">")[0].split('="')[1:]
        
        for n in ontology:
                n = n.split('"')[0]
                
                n = remove_suffix(n)
                
                imports_list.append(n)
                
        return imports_list
    
    except IndexError:
        imports_list=['IndexError']
        
def check_forbidden_uris(uri):
    
    forbidden_uris = ['http://www.w3.org/2002/07/owl#', 
                      'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 
                      'http://www.w3.org/2000/01/rdf-schema#',
                      'http://www.w3.org/XML/1998/namespace',
                      'http://www.w3.org/2001/XMLSchema#'
                      ]
    for n in forbidden_uris:
        if n not in uri:
            return True
        else:
            return False
        
def remove_suffix(uri):
    
    if uri[-1]=='#':
        uri = uri[:-1]
    if uri[-1]=='/':
        uri = uri[:-1]
        
    return uri

# Knowledge graph functions

def construct_graph(path = "data/kg.ttl", format="ttl"):
    g = Graph()
    EONA = Namespace("http://www.eona-x.eu/ontology/tracking/")
    g.bind("eona", EONA)
    g.parse(path=path, format=format)
    
    return g

def filter_graph(g):
    subgraph = Graph()
    subgraph.bind("eona", EONA)
    
        # keep only eona:imports relations
    
    subgraph += g.triples((None, EONA.imports, None))
    
        # remove forbidden uris
    
    for n in forbidden_uris:
        subgraph.remove((None, None, Literal(n)))
        subgraph.remove((None, None, URIRef(n)))
    
    return subgraph

def draw_graph(g):
    nx_graph = rdflib_to_networkx_multidigraph(g)
    
        # drawing
    
    options = {
        'node_color': 'white',
        'node_size': 200,
        'width': 1.2,
    }
    
    plt.figure(figsize=(19.2,10.8*1.2))
    nx.draw_circular(nx_graph, with_labels=True)
    plt.tight_layout()
    plt.savefig('data/kg.svg', format='svg', transparent=True)