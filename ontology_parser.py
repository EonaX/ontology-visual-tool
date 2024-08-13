#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 18:12:46 2024

@author: maximeb
"""
import pandas as pd
from ontology_functions import *

df = pd.read_csv('database.csv', index_col=0)
url = df.iloc[0]['download_url']

    # extract imports from all urls
    
        # ttl parsing

mask = df['syntax'] == 'Turtle'

df['imports_ttl']=df[mask].apply(lambda x: extract_imports_ttl(x['download_url']), axis=1)

        # rdf parsing

mask = df['syntax'] == 'RDF/XML'

df['imports_rdf']=df[mask].apply(lambda x: extract_imports_rdf(x['download_url']), axis=1)


    # dataframe manipulation to get one column

df['imports'] = df['imports_ttl'].combine_first(df['imports_rdf'])

df.drop(['imports_ttl', 'imports_rdf'], axis=1, inplace=True)

    # export

df.to_csv('database_with_imports.csv')
