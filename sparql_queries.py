#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 11:12:06 2024

@author: maximeb
"""

imports_further = r"""
CONSTRUCT {
?provname eona:imports ?provnameImports, ?imports.
}    

WHERE {
?s a eona:Ontology;
eona:isProvidedBy ?prov;
eona:isNamed ?name;
eona:imports ?imports, ?importsNamed. 

OPTIONAL {
?importsNamed eona:isNamed ?nameImports;
eona:isProvidedBy ?provImports.
}


# exclude reflexive triples:
FILTER(!(?s = ?imports)) 
FILTER(!(?imports = ?importsNamed))

# exclude standard imports:
FILTER( ! (?imports = <http://www.w3.org/2002/07/owl>) )
FILTER( ! (?imports =<http://www.w3.org/2001/XMLSchema>) )
FILTER( ! (?imports =<http://www.w3.org/XML/1998/namespace>) )
FILTER( ! (?imports =<http://www.w3.org/2000/01/rdf-schema>) )
FILTER( ! (?imports =<http://www.w3.org/1999/02/22-rdf-syntax-ns>) )

# concat provider and name of the ontology
BIND(CONCAT(?prov, '\n', ?name) AS ?provname )
BIND(CONCAT(?provImports, '\n', ?nameImports) AS ?provnameImports )
       }
"""


imports_near = r"""
CONSTRUCT {
?provname eona:imports ?provnameImports.
}    

WHERE {
?s a eona:Ontology;
eona:isProvidedBy ?prov;
eona:isNamed ?name;
eona:imports ?imports. 

?imports eona:isNamed ?nameImports;
eona:isProvidedBy ?provImports.

# exclude reflexive triples:
FILTER(!(?s = ?imports)) 

# exclude standard imports:
FILTER( ! (?imports = <http://www.w3.org/2002/07/owl>) )
FILTER( ! (?imports =<http://www.w3.org/2001/XMLSchema>) )
FILTER( ! (?imports =<http://www.w3.org/XML/1998/namespace>) )
FILTER( ! (?imports =<http://www.w3.org/2000/01/rdf-schema>) )
FILTER( ! (?imports =<http://www.w3.org/1999/02/22-rdf-syntax-ns>) )

# concat provider and name of the ontology
BIND(CONCAT(?prov, '\n', ?name) AS ?provname )
BIND(CONCAT(?provImports, '\n', ?nameImports) AS ?provnameImports )
       }
"""