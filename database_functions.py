#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 12:21:36 2024

@author: maximeb
"""
import re

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
    error_message = check_constraints(list_of_properties)
    
    if error_message:
        return error_message
    
    apply_constraints(list_of_properties)
    
    df.loc[len(df)] = list_of_properties
    df.to_csv('data/database.csv')

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
    df.to_csv('data/database.csv')
    
    return df

def apply_constraints(list_of_properties):
    """
    Automatic changes applied to the different fields.

    Parameters
    ----------
    list_of_properties : TYPE
        DESCRIPTION.

    Returns
    -------
    list_of_properties : TYPE
        DESCRIPTION.

    """
    list_of_properties[0] = list_of_properties[0].title()
    list_of_properties[1] = list_of_properties[1].title()
    return list_of_properties

def check_constraints(list_of_properties):
    """
    Checks if the constraints are respected.

    Parameters
    ----------
    list_of_properties : TYPE
        DESCRIPTION.

    Returns
    -------
    error_message : TYPE
        DESCRIPTION.

    """
    
    if list_of_properties[0] == "" or list_of_properties[0] == None:
        error_message = 'Name is empty.'
        return error_message
    if list_of_properties[1] == "" or list_of_properties[1] == None:
        error_message = 'Provider is empty.'
        return error_message
    if list_of_properties[3].startswith('http://') == False and list_of_properties[3].startswith('https://') == False:
        error_message = 'Base URI address not valid.'
        return error_message
    if list_of_properties[4].startswith('http://') == False and list_of_properties[4].startswith('https://') == False:
        error_message = 'Download URL address not valid.'
        return error_message