#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 12:21:36 2024

@author: maximeb
"""

def add_ontology(df, list_of_properties):
    """
    Add an ontology to the database.

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    list_of_properties : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    df.loc[len(df)] = list_of_properties
    df.to_csv('database.csv')
    return df

def remove_ontology(df, index_number):
    """
    Remove an ontology from the database based on the index provided.

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    index_number : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    df.drop(index=index_number, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv('database.csv')
    
    return df

def check_constraints(list_of_properties):
    return