import ontoenv
import rdflib
REF = rdflib.URIRef("https://brickschema.org/schema/Brick/ref")
env = ontoenv.OntoEnv(search_directories=["model/"])
graph = rdflib.Graph()
graph.parse("model/all.ttl", format="ttl")
env.import_dependencies(graph)

# clean up ontology defs and their imports that aren't the core 'ref' schema
graph.remove((None, rdflib.OWL.imports, None))
graph.remove((None, rdflib.RDF.type, rdflib.OWL.Ontology))
graph.add((REF, rdflib.RDF.type, rdflib.OWL.Ontology))
for ont, imp in graph.subject_objects(rdflib.OWL.imports):
    if ont != REF:
        graph.remove((ont, rdflib.OWL.imports, imp))

# import all 'units' definitions from imports/bacnet.ttl
# bacnet = rdflib.Graph()
# BACNET = rdflib.Namespace("http://data.ashrae.org/bacnet/2020#")
# bacnet.parse("imports/bacnet.ttl", format="ttl")
# for unit in bacnet.subjects(predicate=rdflib.RDF.type, object=BACNET.EngineeringUnitsEnumerationValue):
#     graph += bacnet.cbd(unit)

graph.serialize("build/ref-schema.ttl", format="ttl")
