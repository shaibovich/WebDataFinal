import rdflib

#######################################################################
#                          PROGRAM CONST                              #
#######################################################################
URL_PREFIX = 'http://example.org/'
FILE_NAME = "ontology.nt"  # TODO: check how the question now what is the ontology.
CREATE_ONTOLOGY = "create"
QUESTION_ONTOLOGY = "question"

#######################################################################
#                        CONSOLE KEY WORDS                            #
#######################################################################
BORN_KEY = "born?"
PRESIDENT_KEY = "president"
AREA_KEY = "area"
GOVERNMENT_KEY = "government"
POPULATION_KEY = "population"
PRIME_KEY = "prime"
MINISTER_KEY = "minister"
CAPITAL_KEY = "capital"

#######################################################################
#                       SENTENCE KEY WORDS                            #
#######################################################################
WHEN_KEY = "when"
WAS_KEY = "was"
WHAT_KEY = "what"
WHO_KEY = "who"
IS_KEY = "is"
OF_KEY = "of"
THE_KEY = "the"

#######################################################################
#                       ONTOLOGY_RELATIONS                            #
#######################################################################
PRESIDENT = rdflib.URIRef(URL_PREFIX + 'presidentOf')
PRIME_MINISTER = rdflib.URIRef(URL_PREFIX + 'primeMinisterOf')
POPULATION = rdflib.URIRef(URL_PREFIX + 'population')
AREA = rdflib.URIRef(URL_PREFIX + 'area')
GOVERNMENT = rdflib.URIRef(URL_PREFIX + 'government')
CAPITAL = rdflib.URIRef(URL_PREFIX + 'capitalOf')
