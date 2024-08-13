#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 18:41:47 2024

@author: maximeb
"""

import requests

def extract_imports_ttl(url):
    r = requests.get(url)

    ontology = r.text

    ontology = ontology.split('prefix')[1:]

    imports_list = []

    for n in ontology:
        try:
            n = n.split('<')[1]
            n = n.split('>')[0]
            imports_list.append(n)
        except IndexError:
            imports_list = ['IndexError']
            
    return imports_list

def extract_imports_rdf(url="http://xmlns.com/foaf/spec/index.rdf"):
    r = requests.get(url)

    ontology = r.text
    
    imports_list = []
          
    try:
        
        # multiple split to isolate base uris
        
        ontology = ontology.split('<rdf:RDF ')[1].split(">")[0].split('="')[1:]
        
        for n in ontology:
                n = n.split('"')[0]
                imports_list.append(n)
                
        return imports_list
    
    except IndexError:
        imports_list=['IndexError']