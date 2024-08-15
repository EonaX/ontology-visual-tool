#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 18:12:46 2024

@author: maximeb
"""

import pandas as pd
from datetime import datetime
from graph_functions import *
from database_functions import *

df = pd.read_pickle('data/df.pkl')
url = df.iloc[0]['download_url']

    # extract imports from all urls
    
        # ttl parsing

mask = df['last_modified'] == 'never'

df['imports']=df['imports'].combine_first(df[mask].apply(lambda x: extract_imports(x['download_url'], x['syntax']), axis=1))
df.loc[mask, 'last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

df['count_uri'] = df['imports'].apply(lambda x : count_imports(x))
    # ad hoc base uri standardization

df['base_uri'] = df['base_uri'].apply(lambda x: remove_suffix(x))

    # export

df.to_pickle('data/df.pkl')
