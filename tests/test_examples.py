"""
Performs validation of the model/schema and data files in the repo
"""
import glob
import os
import logging
import rdflib
import pyshacl
from warnings import warn

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_data_validation(data_file):
    """
    Validates the graphs in the data/ folder against the data and model shapes

    WARNS but does not fail the test on a validation error for a shape with sh:Info severity
    """
    data_graph = rdflib.Graph()

    # validate each data file independently
    data_graph.parse(data_file, format="turtle")
    # load in ref-schema
    data_graph.parse("build/ref-schema.ttl", format="turtle")
    logger.info("Validating data definition of %s ( %d triples)", data_file, len(data_graph))
    valid, x, res_text = pyshacl.validate(
        data_graph=data_graph, advanced=True, js=True, allow_warnings=True
    )
    if not valid:
        data_graph.serialize(f"/tmp/{os.path.basename(data_file)}", format="ttl")
        assert valid, f"{data_file}:\n{res_text}"
