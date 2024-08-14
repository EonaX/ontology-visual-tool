#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 19:44:14 2024

@author: maximeb
"""

from rdflib import URIRef, BNode, Literal, Graph
from rdflib import Namespace
from rdflib.namespace import RDF
import pandas as pd

df = pd.read_pickle('data/df.pkl') 

EONA = Namespace("http://www.eona-x.eu/ontology/tracking/")
kg_ontology = Graph()
kg_ontology.bind("eona", EONA)
    # Instances creation
        
        # set of unique URIs

set_uris = set()

for list_of_uris in df['imports']:
    if type(list_of_uris)==list:
        for uri in list_of_uris:
            set_uris.add(uri)

        # instantiations of Ontology class

for n in set_uris:
    kg_ontology.add((URIRef(n), RDF.type, EONA.Ontology))

    # Properties creation 
    
        # interlinking ontologies with eona:imports object property

for base_uri in df['base_uri']:
           
    mask = df['base_uri'] == base_uri

    for list_of_uris in df[mask]['imports']:
        if type(list_of_uris)==list:
            for uri in list_of_uris:
                uri = URIRef(uri)
                kg_ontology.add((URIRef(base_uri), EONA["imports"], uri))
             
        # adding data property
    
for base_uri in df['base_uri']:
    
    mask = df['base_uri'] == base_uri
    
    kg_ontology.add((URIRef(base_uri), EONA.isNamed, Literal(df[mask].iloc[0]['name'])))
    kg_ontology.add((URIRef(base_uri), EONA.isProvidedBy, Literal(df[mask].iloc[0]['provider'])))
    kg_ontology.add((URIRef(base_uri), EONA.hasDomain, Literal(df[mask].iloc[0]['domain'])))
    kg_ontology.add((URIRef(base_uri), EONA.hasBaseUri, Literal(df[mask].iloc[0]['base_uri'])))
    kg_ontology.add((URIRef(base_uri), EONA.hasDownloadUrl, Literal(df[mask].iloc[0]['download_url'])))
    kg_ontology.add((URIRef(base_uri), EONA.isSerializedIn, Literal(df[mask].iloc[0]['syntax'])))

    # Save KG

kg_ontology.serialize(destination="data/kg.ttl")