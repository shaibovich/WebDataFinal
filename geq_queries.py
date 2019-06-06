import rdflib

from const import FILE_NAME


def convert_to_list(answers, param, original=False):
    lst = []
    for ans in answers:
        with_prefix = ans.asdict().get(param).capitalize()
        with_prefix = with_prefix.split('/')[-1].replace('_', ' ')
        lst.append(with_prefix)
    if len(lst) == 0:
        return "None"
    else:
        if original:
            return lst
        else:
            return ",".join(lst)


def president_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').title().strip()
    ans = list(g.query("select ?president {" + \
                       " ?president <http://example.org/presidentOf> <http://example.org/{}> ".format(arg) + \
                       " } "))
    g.close()

    # TODO: fix
    return convert_to_list(ans, 'president').title()


def prime_minister_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').title().strip()
    ans = list(g.query("select ?prime {" + \
                       " ?prime <http://example.org/primeMinisterOf> <http://example.org/{}> ".format(arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, 'prime').title()


def population_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').strip()
    ans = list(g.query("select ?population {" + \
                       " <http://example.org/{}> <http://example.org/population> ?population ".format(arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, "population")


def area_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').strip()
    ans = list(g.query("select ?area {" + \
                       " <http://example.org/{}> <http://example.org/area> ?area .".format(arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, "area")


def government_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').title()
    ans = list(g.query("select ?gov {" + \
                       " <http://example.org/{}> <http://example.org/government> ?gov ".format(arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, "gov").title()


def capital_of_country_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').title()
    ans = list(g.query("select ?cap {" + \
                       " ?cap <http://example.org/capitalOf> <http://example.org/{}> .".format(arg) + \
                       " } "))
    g.close()
    return convert_to_list(ans, "cap").title()


def president_born_date_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').title()
    ans = list(g.query("select ?bod {" + \
                       " ?president <http://example.org/presidentOf> <http://example.org/{}> .".format(arg) + \
                       " ?president <http://example.org/birthDate> ?bod ." + \
                       " } "))
    g.close()
    return convert_to_list(ans, "bod")


def prime_minister_born_date_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').title()
    ans = list(g.query("select ?bod {" + \
                       " ?prime <http://example.org/primeMinisterOf> <http://example.org/{}> .".format(arg) + \
                       " ?prime <http://example.org/birthDate> ?bod ." + \
                       " } "))
    g.close()
    return convert_to_list(ans, "bod")


def who_query(arg):
    g = rdflib.Graph()
    g.parse(FILE_NAME, format="nt")
    arg = arg.replace(' ', '_').title()
    president = check_if_president(g, arg)
    prime = check_if_prime_minister(g, arg)
    if prime is False and president is False:
        return "None"
    elif prime is not False:
        output = "Prime minister of "
        if len(prime) == 1:
            return output + prime[0].title()
        return output + ", ".join(prime)[:-1].title()
    else:
        output = "President of "
        if len(president) == 1:
            return output + president[0].title()
        return output + ", ".join(president)[:-1].title()



def check_if_prime_minister(g, person):
    ans = list(g.query("select ?country  {" + \
                       " <http://example.org/{}> <http://example.org/primeMinisterOf> ?country .".format(person) + \
                       " } "))
    if len(ans) == 0:
        return False
    return convert_to_list(ans,"country",True)

def check_if_president(g, person):
    ans = list(g.query("select ?country  {" + \
                       " <http://example.org/{}> <http://example.org/presidentOf> ?country .".format(person) + \
                       " } "))
    if len(ans) == 0:
        return False
    return convert_to_list(ans,"country",True)


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


