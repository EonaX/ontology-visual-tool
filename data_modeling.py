#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:35:09 2024

@author: maximeb
"""

import pandas as pd
from pandas.io.json._table_schema import build_table_schema
import json

# pandas data modeling

df_schema = pd.DataFrame(
    {
     "name":pd.Series(dtype='str'),
     "provider":pd.Series(dtype='str'),
     "domain":pd.Series(dtype='str'),
     "base_uri":pd.Series(dtype='str'),
     "download_url":pd.Series(dtype='str'),
     "syntax":pd.Series(dtype='str'),
     }
    )

    # csv export

df_schema.to_csv('database.csv')

    # json schema export

json_schema =json.dumps(build_table_schema(df_schema, version=False), indent=4)

with open('ontology.schema', "w") as f:
    f.write(json_schema)

