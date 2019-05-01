import rdflib
import requests
import lxml.html
from rdflib import Literal, XSD
from const import URL_PREFIX

prefix = 'https://en.wikipedia.org/'
g = rdflib.Graph()

def add_relation_to_graph(subject, predicate, objec):
    objec = objec.replace(' ', '_')
    subject = subject.replace(' ', '_')
    g.add((createUriRef(subject), predicate, createUriRef(objec)))


def createUriRef(end_point):
    return rdflib.URIRef(URL_PREFIX+ end_point)








def start(file_path):
    print("START INIT ONTOLOGY , WILL SAVE AT {}".format(file_path))
