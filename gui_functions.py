#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 14:40:46 2024

@author: maximeb
"""
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go


def set_page_config():
    """
    Layout configuration settings.

    Returns
    -------
    None.

    """
    st.set_page_config(
        page_title="Real-Time Data Science Dashboard",
        page_icon="docs/logo-eona.png",
        layout="centered",
    )

def count_line_graph(df):
    count_df = df.groupby(['added_when']).count()
    fig = px.line(count_df, 
                  x=count_df.index, 
                  y=count_df['name'],                   
                  height=300,
                  labels = {
                      'added_when': 'Date',
                      'name': 'Count'
                      })
                    
    
    fig.update_layout(
        title = '<b>Ontology Count Over Time</b>',

        )
    return fig

def ontology_count_metric(df):

    count = len(df)    
    
    fig = go.Figure(go.Indicator(
        
        mode = "number",
        value = count
        ))
    
    fig.update_layout(
        title = '<b>Total Ontology Count</b>',
        margin=dict(l=20, r=20, t=55, b=250),
        )

    
    return fig