import rdflib
from const import FILE_NAME, URL_PREFIX
from rdflib import XSD


def convert_to_list(answers, param):
    lst = []
    for ans in answers:
        with_prefix = ans.asdict().get(param).capitalize()
        with_prefix = with_prefix.split('/')[-1].replace('_', ' ').title()
        lst.append(with_prefix)
    if len(lst) == 0:
        return "None"
    else:
        return lst[0]


def president_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').lower()
    ans = list(g.query("select ?president {" + \
                       " ?president <http://example.org/presidentOf> ?country ." + \
                      "FILTER (regex(lcase(str(?country)), '{}') && strlen(str(?country)) != strlen('{}'))".format(arg,arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, 'president')


def prime_minister_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').lower()
    ans = list(g.query("select ?prime {" + \
                       " ?prime <http://example.org/primeMinisterOf> ?country ." + \
                        "FILTER (regex(lcase(str(?country)), '{}') && strlen(str(?country)) != strlen('{}'))".format(arg,arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, 'prime')


def population_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').lower()
    ans = list(g.query("select ?population {" + \
                       " ?country <http://example.org/population> ?population ." + \
                        "FILTER (regex(lcase(str(?country)), '{}') && strlen(str(?country)) != strlen('{}'))".format(arg,arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, "population")


def area_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').lower()
    ans = list(g.query("select ?area {" + \
                       " ?country <http://example.org/area> ?area ." + \
                        "FILTER (regex(lcase(str(?country)), '{}') && strlen(str(?country)) != strlen('{}'))".format(arg,arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, "area")


def government_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').lower()
    ans = list(g.query("select ?gov {" + \
                       " ?country <http://example.org/government> ?gov ." + \
                        "FILTER (regex(lcase(str(?country)), '{}') && strlen(str(?country)) != strlen('{}'))".format(arg,arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, "gov")


def capital_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').lower()
    ans = list(g.query("select ?cap {" + \
                       " ?cap <http://example.org/capitalOf> ?country ." + \
                        "FILTER (regex(lcase(str(?country)), '{}') && strlen(str(?country)) != strlen('{}'))".format(arg,arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, "cap")


def president_born_date_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').lower()
    ans = list(g.query("select ?bod {" + \
                       " ?president <http://example.org/presidentOf> ?country ." + \
                       " ?president <http://example.org/birthDate> ?bod ." + \
                        "FILTER (regex(lcase(str(?country)), '{}') && strlen(str(?country)) != strlen('{}'))".format(arg,arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, "bod")


def prime_minister_born_date_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').lower()
    ans = list(g.query("select ?bod {" + \
                       " ?prime <http://example.org/primeMinisterOf> ?country ." + \
                       " ?prime <http://example.org/birthDate> ?bod ." + \
                        "FILTER (regex(lcase(str(?country)), '{}') && strlen(str(?country)) != strlen('{}'))".format(arg,arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, "bod")


def who_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').lower()
    president = check_if_president(g, arg)
    prime = check_if_prime_minister(g, arg)
    if prime is False and president is False:
        return "None"
    elif prime is not False:
        return "Prime minister of {}".format(prime)
    else:
        return "President of {}".format(president)



def check_if_prime_minister(g, person):
    ans = list(g.query("select ?country  {" + \
                       " ?prime <http://example.org/primeMinisterOf> ?country ." + \
                        "FILTER (regex(lcase(str(?prime)), '{}') && strlen(str(?prime)) != strlen('{}'))".format(person, person) + \
                       " } "))
    if len(ans) == 0:
        return False
    return convert_to_list(ans,"country")

def check_if_president(g, person):
    ans = list(g.query("select ?country  {" + \
                       " ?president <http://example.org/presidentOf> ?country ." + \
                        "FILTER (regex(lcase(str(?president)), '{}') && strlen(str(?president)) = strlen('{}'))".format(person, person) + \
                       " } "))
    if len(ans) == 0:
        return False
    return convert_to_list(ans,"country")


#####################################################
#                    Question b                     #
#####################################################


def number_of_presidents():
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    ans = list(g.query("select (count(distinct ?president) as ?total) {" + \
                       " ?president <http://example.org/presidentOf> ?country " + \
                       " } "))[0]
    g.close()
    ans = ans.asdict().get('total').capitalize()
    print('Number of president : {}'.format(ans))


def number_of_countires():
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    ans = list(g.query("select (count(distinct ?country) as ?total) {" + \
                       " ?president <http://example.org/presidentOf> ?country " + \
                       " } "))[0]
    g.close()
    ans = ans.asdict().get('total').capitalize()
    print('Number of countries : {}'.format(ans))


def number_of_republic_countires():
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    ans = list(g.query("select (count(distinct ?government) as ?total) {" + \
                       " ?country <http://example.org/government> ?government " + \
                       "FILTER (regex(lcase(str(?government)), 'republic'))" + \
                       " } "))[0]
    g.close()
    ans = ans.asdict().get('total').capitalize()
    print('Number of republic countries : {}'.format(ans))


def number_of_monarchy_countries():
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    ans = list(g.query("select (count(distinct ?government) as ?total) {" + \
                       " ?country <http://example.org/government> ?government " + \
                       "FILTER (regex(lcase(str(?government)), 'monarchy'))" + \
                       " } "))[0]
    g.close()
    ans = ans.asdict().get('total').capitalize()
    print('Number of monarchy countries : {}'.format(ans))

# president_of_country_query("israel")
who_query("Donald Trump")
