import rdflib
import requests
import lxml.html
from rdflib import Literal, XSD
from const import *

prefix = 'https://en.wikipedia.org/'

# Create new Ontoloty
g = rdflib.Graph()


def add_relation_to_graph(subject, predicate, objec):
    objec = objec.replace(' ', '_')
    subject = subject.replace(' ', '_')
    g.add((createUriRef(subject), predicate, createUriRef(objec)))


def createUriRef(end_point):
    return rdflib.URIRef(URL_PREFIX+ end_point)

# Returns Capital Name
def get_capital(table):
    capital = table.xpath("./tbody/tr/th[text() = 'Capital']/../td/a/text() | ./tbody/tr/th[text() = 'Capital']/../td/div/ul/li/a/text()")
    return capital

# Returns President Name and Born date if exists as a tuple (President name, Born date)
def get_president(table):
    # president name
    president = table.xpath("./tbody/tr[th/div/a[text() = 'President']]/td//a/text()")

    if president!= None and len(president) >0:
         # president Born date
        president_born_date_page = prefix + table.xpath("./tbody/tr[th/div/a[text() = 'President']]/td//a/@href")[0]
        # print(president_born_date_page)

         # patches - few more...
        #  ivory coast patch....
        if president_born_date_page == 'https://en.wikipedia.org//w/index.php?title=Alassane_Outtara&action=edit&redlink=1':
            president_born_date_page = 'https://en.wikipedia.org/wiki/Alassane_Ouattara'
        # David Panuelo path  - Federated_States_of_Micronesia has no link to him
        if president[0] == 'David Panuelo':
            return (president[0],None)

        # get president born date
        res = requests.get(president_born_date_page)
        doc = lxml.html.fromstring(res.text)
        president_born_date_table = doc.xpath("//table[contains(@class, 'infobox')]")[0]
        president_born_date = president_born_date_table.xpath("//tbody/tr[th[text() = 'Born']]/td/text()")
        if len(president_born_date)>0:
            return (president[0],president_born_date[0])
        else:
            return (president[0],None)
    else:
        return (None,None)


# Returns prime_minister Name and Born date if exists as a tuple (prime_minister name, Born date)
def get_prime_minister(table):
    # gets prime minister name
    prime_minister = table.xpath("./tbody/tr[th/div/a[text() = 'Prime Minister']]/td//a/text()")
    if  prime_minister != None and len(prime_minister) >0:

        #path
        # 	Central African Republic patch - no link to prime minister
        if (prime_minister[0] == 'Firmin Ngrébada'):
            return (prime_minister[0],None)
        else:
            # get prime minister born date
            prime_minister_born_date_page = prefix + table.xpath("./tbody/tr[th/div/a[text() = 'Prime Minister']]/td//a/@href")[0]
            res = requests.get(prime_minister_born_date_page)
            doc = lxml.html.fromstring(res.text)
            prime_minister_born_date_table = doc.xpath("//table[contains(@class, 'infobox')]")[0]
            prime_minister_born_date = prime_minister_born_date_table.xpath("//tbody/tr[th[text() = 'Born']]/td/text()")
            return (prime_minister[0],prime_minister_born_date[0])
    else:
        return (None,None)

# Returns country Pupulation
def get_population(table):
    population = table.xpath("./tbody/tr[th/a[text() = 'Population']]/following-sibling::tr[1]/td/text()[1]")
    if len(population) > 0:
        return population[0]
    else:
        return None

# Returns country Area
def get_area(table):
    area = table.xpath("./tbody/tr[th/a[contains(text(), 'Area')]]/following-sibling::tr[1]/td/text()[1]")
    if len(area) > 0:
        return area[0]
    else:
        return None

# Returns country goverment - FOR NOW RETURNNING ALL THE WORDS AS A STRING WITH SPACES< TO CHECK WHAT SHOULD WE DO WITH THAT
def get_government(table):
    government = table.xpath("./tbody/tr[th/a[contains(text(), 'Government')]]/td/a/text()")
    if len(government) > 0:
        return (" ").join(government)
    else:
        return None

def extract_country_data(country_name,country_link):
    res = requests.get(country_link)
    doc = lxml.html.fromstring(res.text)
    table = doc.xpath("//table[contains(@class, 'infobox')]")[0]
    capital = get_capital(table)
    for cap in capital:
        add_relation_to_graph(cap,CAPITAL,country_name)
    president,president_born = get_president(table)
    prime_minister,prime_minister_born  = get_prime_minister(table)
    population = get_population(table)
    area = get_area(table)
    government = get_government(table)

    #NOW NEED TO ADD RELATIONS TO ONRTOLOGY




    # if (president != None):
    #         print(president,"          PRESIDENT")
    # if prime_minister != None:
    #         print(prime_minister,"        PRIME MINISTER")
    # if (population != None):
    #         print(population,"        PoPULATION")
    # if (area != None):
    #         print(area,"           AREA")
    # if (government != None):
    #     print(government, "           GOVERNMENT")
    # if(president_born != None ):
    #     print(president_born,"           PRESIDENT BORN AT: ")
    # if(prime_minister_born != None ):
    #     print(president_born,"         PRIME MINISTER BORN AT: ")
    #



def start(file_path):
    #to ask shay about the next lint perpuse
    # print("START INIT ONTOLOGY , WILL SAVE AT {}".format(file_path))
    res = requests.get(COUNTRY_URL)
    doc = lxml.html.fromstring(res.text)
    country_table = doc.xpath("//table[contains(@class, 'wikitable')]")[0]
    # path - entering to many lines..
    countries =  country_table.xpath("//tbody/tr")[3:236]
    # i = 0
    for country in countries:
        # i = i + 1
        # print ("**********",i,"******************")
        country_link = country.xpath("./td[2]//a/@href")[0]
        country_name = country.xpath("./td[2]//a/text()")[0].replace(" ","")
        createUriRef(country_name)
        print("hello")
        print(country_name);

        extract_country_data(country_name,prefix+country_link)

   # g.serialize()





start("hello.txt")
# extract_country_data("Central_African_Republic","https://en.wikipedia.org/wiki/Federated_States_of_Micronesia")
# res = requests.get("https://en.wikipedia.org/wiki/South_Africa")
