import rdflib
import requests, datetime, re
import lxml.html
from rdflib import Literal, XSD
from const import *

prefix = 'https://en.wikipedia.org/'


def add_relation_to_graph(g, subject, predicate, objec):
    objec = objec.replace(' ', '_')
    subject = subject.replace(' ', '_')
    g.add((createUriRef(subject), predicate, createUriRef(objec)))


def createUriRef(end_point):
    return rdflib.URIRef(URL_PREFIX + end_point)


# Returns Capital Name
def get_capital(table):
    capital = table.xpath(
        "./tbody/tr/th[text() = 'Capital']/../td/a/text() | ./tbody/tr/th[text() = 'Capital']/../td/div/ul/li/a/text()")
    return capital

def get_country_name(table):
    name = table.xpath('//h1[contains(@id,"firstHeading")]/text()')[0].strip()
    if '(' in name:
        name = name.split('(')[0].strip()
    return name


def get_date_string(date_string):
    day, month, year = None, None, None
    date_list = date_string.replace(',', '').split(' ')
    # first getting the month
    for date in date_list:
        if re.search('[a-zA-Z]', date) != None:
            month = date
            break
    if month is None or len(date_list) != 3 or date_string.count('age') > 0:
        return
    date_list.remove(month)
    # day will be in length of 2, year will be in length of 4
    if len(date_list[0]) == 4:
        year = date_list[0]
        day = date_list[1]
    else:
        year = date_list[1]
        day = date_list[0]

    new_date = day + ' ' + month + ' ' + year

    return datetime.datetime.strptime(new_date, '%d %B %Y').strftime("%Y-%m-%d")


# Returns President Name and Born date if exists as a tuple (President name, Born date)
def get_president(g, country_name, table):
    president_element = table.xpath("./tbody/tr[th/div/a[text() = 'President']]")
    if len(president_element) > 0:
        presidnet = president_element[0].xpath("./td//a[contains(@href,'wiki')]")
        if len(presidnet) == 0:
            president_name = president_element[0].xpath("./td//a/text()")[0].strip()
        else:
            presidnet_url = presidnet[0].xpath("./@href")[0]
            president_name = get_president_data(g, presidnet_url)

        add_relation_to_graph(g, president_name, PRESIDENT, country_name)


def get_president_data(g, president_url):
    res = requests.get(prefix + president_url)
    doc = lxml.html.fromstring(res.text)
    president_name = get_country_name(doc)
    table = doc.xpath("//table[contains(@class, 'infobox')]")[0]
    born = table.xpath(".//tbody/tr[th[text() = 'Born']]")
    if len(born) > 0:
        born_element = born[0]
        born_date = born_element.xpath('./td/text()')[0]
        born_date = get_date_string(born_date)
        if born_date is not None:
            dob = Literal(born_date, datatype=XSD.date)
            add_relation_to_graph(g, president_name, BIRTH_DATE, dob)
    return president_name


# Returns prime_minister Name and Born date if exists as a tuple (prime_minister name, Born date)
def get_prime_minister(g, country_name, table):
    prime_minister_element = table.xpath("./tbody/tr[th/div/a[text() = 'Prime Minister']]")
    if len(prime_minister_element) > 0:
        prime_minister = prime_minister_element[0].xpath("./td//a[contains(@href,'wiki')]")
        if len(prime_minister) == 1:
            prime_minister_url = prime_minister[0].xpath("./@href")[0]
            prime_minister_name = get_president_data(g, prime_minister_url)
        else:
            prime_minister_name = prime_minister_element[0].xpath("./td//text()")[0].strip()

        add_relation_to_graph(g, prime_minister_name, PRIME_MINISTER, country_name)



# Returns country Pupulation
def get_population(g, country_name, table):
    population = table.xpath("./tbody/tr[th/a[contains(text(), 'Population')]]/following-sibling::tr[1]/td/text()[1]")
    if len(population) == 0:
        population = table.xpath(".//tr[th[contains(text(), 'Population')]]/following-sibling::tr[1]/td/text()[1]")
    if len(population) == 0:
        return
    else:
        population_number = population[0].strip()
        if '(' in population_number:
            population_number = population_number.split('(')[0].strip()
        add_relation_to_graph(g, country_name, POPULATION, population_number)


# Returns country Area
def get_area(g, country_name, table):
    area = table.xpath("./tbody/tr[th/a[contains(text(), 'Area')]]/following-sibling::tr[1]/td/text()[1]")
    if len(area) == 0:
        area = table.xpath("./tbody/tr[th[contains(text(), 'Area')]]/following-sibling::tr[1]/td/text()[1]")
    if len(area) == 0:
        return
    else:
        if len(area[0].split('(')) == 1:
            area_final_size = area[0]
            if 'km' not in area_final_size:
                area_final_size += '_km'
        else:
            area_list = area[0].split('(')
            area_final_size = 0
            for area_size in area_list:
                if area_size.count('km') > 0:
                    area_final_size = area_size
        area_final_size += '2'
        add_relation_to_graph(g, country_name, AREA, area_final_size)


# Returns country goverment - FOR NOW RETURNNING ALL THE WORDS AS A STRING WITH SPACES< TO CHECK WHAT SHOULD WE DO WITH THAT
def get_government(g, country_name, table):
    government = table.xpath("./tbody/tr[th/a[contains(text(), 'Government')]]")
    if len(government) == 0:
        government = table.xpath("./tbody/tr[th[contains(text(), 'Government')]]")
    if len(government) > 0:
        government_name = "_".join(government[0].xpath('.//td/a/text()'))

        add_relation_to_graph(g, country_name, GOVERNMENT, government_name)


def extract_country_data(g, country_name, country_link):
    res = requests.get(country_link)
    doc = lxml.html.fromstring(res.text)
    table = doc.xpath("//table[contains(@class, 'infobox')]")[0]
    capital = get_capital(table)
    for cap in capital:
        add_relation_to_graph(g, cap, CAPITAL, country_name)
    get_president(g, country_name, table)
    get_prime_minister(g, country_name, table)
    get_population(g, country_name, table)
    get_area(g, country_name, table)
    get_government(g, country_name, table)


def start(file_path):
    time = datetime.datetime.now()
    g = rdflib.Graph()
    res = requests.get(COUNTRY_URL)
    doc = lxml.html.fromstring(res.text)
    country_table = doc.xpath("//table[contains(@class, 'wikitable')]")[0]
    countries = country_table.xpath("//tbody/tr")[3:236]
    for country in countries:
        country_link = country.xpath("./td[2]//a/@href")[0]
        country_name = country.xpath("./td[2]//a/text()")[0].strip()
        # print("country [{}] with country href [{}]".format(country_name, country_link))
        extract_country_data(g, country_name, prefix + country_link)

    g.serialize(FILE_NAME, format='nt')
    finish_time = datetime.datetime.now()
    print("Finish after [{}] ".format(finish_time - time))


start("")#
