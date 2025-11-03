import os
import subprocess
from datetime import datetime, timezone

import ontoenv
import rdflib
REF = rdflib.URIRef("https://brickschema.org/schema/Brick/ref")
env = ontoenv.OntoEnv(search_directories=["model/"], temporary=True)
graph = rdflib.Graph()
graph.parse("model/all.ttl", format="ttl")
env.import_dependencies(graph)


def _run_git_command(*args: str) -> str:
    try:
        output = subprocess.check_output(["git", *args], stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""
    return output.decode().strip()


def _get_version_string() -> str:
    tag = os.getenv("CI_COMMIT_TAG", "").strip()
    if tag:
        return tag

    if os.getenv("CI_COMMIT_SHA"):
        branch = os.getenv("CI_COMMIT_BRANCH") or os.getenv("CI_COMMIT_REF_NAME") or "unknown"
        commit = os.getenv("CI_COMMIT_SHA", "unknown").strip()
        timestamp = os.getenv("CI_COMMIT_TIMESTAMP", "").strip()
        return f"git:{branch}@{commit} date:{timestamp}"

    commit = _run_git_command("rev-parse", "HEAD") or "unknown"
    branch = _run_git_command("rev-parse", "--abbrev-ref", "HEAD") or "HEAD"
    timestamp = _run_git_command("show", "-s", "--format=%cI", "HEAD")
    if not timestamp:
        timestamp = datetime.now(timezone.utc).isoformat()
    return f"git:{branch}@{commit} date:{timestamp}"

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

graph.remove((REF, rdflib.OWL.versionInfo, None))
graph.add((REF, rdflib.OWL.versionInfo, rdflib.Literal(_get_version_string())))

graph.serialize("build/ref-schema.ttl", format="ttl")
