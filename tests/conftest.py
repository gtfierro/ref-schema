import pytest
import glob
import pyshacl
import rdflib

def pytest_generate_tests(metafunc):
    if "data_file" in metafunc.fixturenames:
        args = glob.glob("examples/*.ttl")
        metafunc.parametrize("data_file", args)
