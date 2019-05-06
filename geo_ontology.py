import rdflib
import requests
import lxml.html
from rdflib import Literal, XSD
from const import URL_PREFIX,COUNTRY_URL

prefix = 'https://en.wikipedia.org/'
# create new ontoloty
g = rdflib.Graph()

def add_relation_to_graph(subject, predicate, objec):
    objec = objec.replace(' ', '_')
    subject = subject.replace(' ', '_')
    g.add((createUriRef(subject), predicate, createUriRef(objec)))


def createUriRef(end_point):
    return rdflib.URIRef(URL_PREFIX+ end_point)

def extract_country_data(country_name,country_link):
    return 4



def start(file_path):
    #to ask shay about the next lint perpuse
    # print("START INIT ONTOLOGY , WILL SAVE AT {}".format(file_path))
    res = requests.get(COUNTRY_URL)
    doc = lxml.html.fromstring(res.text)
    country_table = doc.xpath("//table[contains(@class, 'wikitable')]")[0]
    # to find whats the problem with the last line..
    countries =  country_table.xpath("//tbody/tr")[3:236]
    # i = 1
    for country in countries:
        # print (i)
        # i = i+1
        country_link = country.xpath("./td[2]//a/@href")[0]
        country_name = country.xpath("./td[2]//a/text()")[0].replace(" ","")
        createUriRef(country_name)
        extract_country_data(country_name,country_link)
        print (country_name,country_link)

   # g.serialize()

start("hello.txt")

