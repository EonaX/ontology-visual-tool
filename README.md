# ontology-visual-tool

This tool provides a visual knowledge graph representation of the ontologies identified as relevant for Eona-X by its members and their interrelations. Its ontology database can be updated by anyone through a graphical user interface reachable on the web, resulting in a modification of the visual representation.

It is composed of three components:
 + a writeable relational database with GUI
 + a graph constructor in the back-end
 + a graph visualizer in the front-end

1. Ontology directory database:
 + ontology data modeling
 + DBMS (pandas)
 + GUI (Streamlit)

2. Graph constructor:
 + RDF/OWL parser
 + RDF knowledge graph constructor

3. Graph visualizer:
 + either vOWL or Neo4J's visual renderer
