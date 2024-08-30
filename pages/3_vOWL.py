#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 09:15:02 2024

@author: maximeb
"""

import streamlit as st
import streamlit.components.v1 as components
from database_functions import *
from gui_functions import *
import pandas as pd

st.set_page_config(layout="wide")

st.title("Ontology Analyser")

df = pd.read_pickle('data/df.pkl')

urls = df['download_url']

option = st.selectbox("Choose an ontology", urls)

components.iframe(f"https://service.tib.eu/webvowl/#iri={option}", height = 1500)
