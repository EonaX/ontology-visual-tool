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
import math
import re

forbidden_uris = ['http://www.w3.org/2002/07/owl', 
                  'http://www.w3.org/1999/02/22-rdf-syntax-ns', 
                  'http://www.w3.org/2000/01/rdf-schema',
                  'http://www.w3.org/XML/1998/namespace',
                  'http://www.w3.org/2001/XMLSchema'
                  ]

# Ontology functions

def download_ontology(url):
    """
    Download the ontology from the given download_url.

    Parameters
    ----------
    url : str
        DESCRIPTION.

    Returns
    -------
    ontology : str
        DESCRIPTION.

    """
    
    r = requests.get(url)

    ontology = r.text
    
    return ontology

def extract_imports_ttl(url):
    """
    Extracts all base URIS of ontologies used in a Turtle-serialized ontology.

    Parameters
    ----------
    url : str
        DESCRIPTION.

    Returns
    -------
    imports_list : TYPE
        DESCRIPTION.

    """
    
    ontology = download_ontology(url)

    ontology = re.split("prefix", ontology, flags=re.IGNORECASE)
        
    ontology = ontology[1:]

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

def extract_imports_rdf(url):
    """
    Extract all base URIS of ontologies used in a RDF/XML-serialized ontology.

    Parameters
    ----------
    url : str, optional
        DESCRIPTION. The default is "http://xmlns.com/foaf/spec/index.rdf".

    Returns
    -------
    imports_list : TYPE
        DESCRIPTION.

    """
    ontology = download_ontology(url)
    
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
        
def extract_imports(url, syntax):
    """
    Extracts prefixes from any kind of RDF serialization.

    Parameters
    ----------
    url : TYPE
        DESCRIPTION.
    syntax : TYPE
        DESCRIPTION.

    Returns
    -------
    imports_list : TYPE
        DESCRIPTION.

    """
    if syntax == 'Turtle':
        imports_list = extract_imports_ttl(url)
        print('ttl imports...')
        return imports_list
    
    if syntax == 'RDF/XML':
        print('rdf/xml imports...')
        imports_list = extract_imports_rdf(url)
        return imports_list
        
def check_forbidden_uris(uri):
    """
    List of all-too-common namespaces.

    Parameters
    ----------
    uri : TYPE
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    """
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
    """
    Remove usual suffixes ('#' and '/') in order to avoid duplicates in graph viz.

    Parameters
    ----------
    uri : TYPE
        DESCRIPTION.

    Returns
    -------
    uri : TYPE
        DESCRIPTION.

    """
    if uri[-1]=='#':
        uri = uri[:-1]
    if uri[-1]=='/':
        uri = uri[:-1]
        
    return uri

# Knowledge graph functions

def construct_graph(path, format): # don't work    
    g = Graph()
    g.parse(path=path, format=format)
    EONA = Namespace("http://www.eona-x.eu/ontology/tracking#")
    g.bind("eona", EONA)
    g.parse(path=path, format=format)
    
    return g

def filter_graph(g, triple=(None, None, None), hide_forbidden_uris=True, hide_reflexive_triples=True):
    """
    Apply graph data manipulations.

    Parameters
    ----------
    g : TYPE
        DESCRIPTION.
    NAMESPACE : TYPE
        DESCRIPTION.
    option : TYPE
        DESCRIPTION.

    Returns
    -------
    subgraph : TYPE
        DESCRIPTION.

    """
    subgraph = Graph()
        # keep only eona:imports relations
    
    subgraph += g.triples(triple)
    
    return subgraph

def remove_forbidden_uris(g):
    for n in forbidden_uris:
        g.remove((None, None, Literal(n)))
        g.remove((None, None, URIRef(n)))
        
    return g
    
def remove_reflexive_triples(g):
    for s, p, o in g:
        if s == o:
            g.remove((s, p, o))
            
    return g

def save_graph(graph, destination):
    """
    Save the graph to the destination given.

    Parameters
    ----------
    graph : rdflib Graph
        DESCRIPTION.
    destination : str
        DESCRIPTION.

    Returns
    -------
    None.

    """
    graph.serialize(destination)
    print(f"saved at {destination}")

def convert_to_nx(rdflib_graph):
    """
    Converts a rdflib graph to a networkx graph.

    Parameters
    ----------
    rdflib_graph : TYPE
        DESCRIPTION.

    Returns
    -------
    nx_graph : TYPE
        DESCRIPTION.

    """
    
    nx_graph = rdflib_to_networkx_multidigraph(rdflib_graph)
    
    return nx_graph

def draw_graph(nx_graph, layout = 'spring'):
    """
    Froma rdflib graph, it displays a Matplotlib graph visualization.

    Parameters
    ----------
    g : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
        # options
            
    node_options = {"node_size": 2500, "edgecolors": "#ffffff92", "linewidths": 2.0, "node_color":"#444444bb"}
    label_options = {"font_size":14, 'font_color':"white"}
    edge_options = {"width":1.5, 'edge_color':"grey", 'arrowsize':30, 'connectionstyle':'arc3,rad=0.2', "node_size": 2500}
    
            # layout
    if layout == 'spring':
        pos = nx.spring_layout(nx_graph, k=4/math.sqrt(nx_graph.order()))
    
    if layout == 'circular':
        pos = nx.circular_layout(nx_graph)

    # pos = nx.nx_agraph.graphviz_layout(nx_graph, prog="neato")
        # plt
    
    plt.figure(figsize=(19.2,10.8))
    plt.axes(frameon=False)
    nx.draw_networkx_nodes(nx_graph, pos, **node_options)
    nx.draw_networkx_labels(nx_graph, pos, **label_options)
    nx.draw_networkx_edges(nx_graph, pos, **edge_options)
    
        # export to svg
    plt.tight_layout()
    plt.savefig('data/kg.svg', format='svg', transparent=True)
    
    return nx_graph