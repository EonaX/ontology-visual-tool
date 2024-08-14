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

def filter_graph(g, NAMESPACE, option):
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
    subgraph.bind("eona", NAMESPACE)
    
        # keep only eona:imports relations
    
    subgraph += g.triples((None, NAMESPACE[option], None))
    
        # remove forbidden uris
    
    for n in forbidden_uris:
        subgraph.remove((None, None, Literal(n)))
        subgraph.remove((None, None, URIRef(n)))
    
    return subgraph

def draw_graph(g):
    """
    Convert to Network-X type that allows matplotlib visualization.

    Parameters
    ----------
    g : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    # conversion
    
    nx_graph = rdflib_to_networkx_multidigraph(g)
    
    # drawing
    
        # options
            
    node_options = {"node_size": 2500, "edgecolors": "grey", "linewidths": 2.0, 'cmap':'viridis'}
    label_options = {"font_size":14, 'font_color':"white"}
    edge_options = {"width":1.5, 'edge_color':"grey", 'arrowsize':15, 'connectionstyle':'arc3,rad=0.2', "node_size": 2500}
    pos = nx.circular_layout(nx_graph)
    
        # plt
    
    plt.figure(figsize=(19.2,10.8*1.2))
    plt.axes(frameon=False)
    nx.draw_networkx_nodes(nx_graph, pos, **node_options)
    nx.draw_networkx_labels(nx_graph, pos, **label_options)
    nx.draw_networkx_edges(nx_graph, pos, **edge_options)
    
        # export to svg
    plt.tight_layout()
    plt.savefig('data/kg.svg', format='svg', transparent=True)
