import ontoenv
import rdflib
env = ontoenv.OntoEnv()
graph = rdflib.Graph()
graph.parse("model/all.ttl", format="ttl")
env.import_dependencies(graph)
graph.serialize("build/ref-schema.ttl", format="ttl")
