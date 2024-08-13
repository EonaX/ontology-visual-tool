#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:35:09 2024

@author: maximeb
"""

import pandas as pd
from pandas.io.json._table_schema import build_table_schema
import json

df = pd.DataFrame(
    {
     "name":["Test Ontology Name"],
     "provider":["Test Ontology Provider"],
     "domain":["Test Domain"],
     "subdomain":["Test Subdomain"],
     "syntax":["ttl"],
     "base_uri":["http://www.example.com/base#"],
     "download_url":["http://www.example/download#"]
     }
    )

json_schema =json.dumps(build_table_schema(df, version=False), indent=4)

with open('ontology.schema', "w") as f:
    f.write(json_schema)
