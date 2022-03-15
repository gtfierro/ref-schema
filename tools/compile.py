import ontoenv
import rdflib
REF = rdflib.URIRef("https://brickschema.org/schema/Brick/ref")
env = ontoenv.OntoEnv()
graph = rdflib.Graph()
graph.parse("model/all.ttl", format="ttl")
env.import_dependencies(graph)
# clean up ontology defs and their imports that aren't the core 'ref' schema
graph.remove((None, rdflib.RDF.type, rdflib.OWL.Ontology))
graph.add((REF, rdflib.RDF.type, rdflib.OWL.Ontology))
for ont, imp in graph.subject_objects(rdflib.OWL.imports):
    if ont != REF:
        graph.remove((ont, rdflib.OWL.imports, imp))

graph.serialize("build/ref-schema.ttl", format="ttl")
