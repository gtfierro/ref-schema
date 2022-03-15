import ontoenv
import rdflib
REF = rdflib.URIRef("https://brickschema.org/schema/Brick/ref")
env = ontoenv.OntoEnv()
graph = rdflib.Graph()
graph.parse("model/all.ttl", format="ttl")
env.import_dependencies(graph)
graph.remove((None, rdflib.RDF.type, rdflib.OWL.Ontology))
graph.add((REF, rdflib.RDF.type, rdflib.OWL.Ontology))
graph.serialize("build/ref-schema.ttl", format="ttl")
