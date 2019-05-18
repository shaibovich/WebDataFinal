from const import BORN_KEY, PRESIDENT_KEY, CAPITAL_KEY, PRIME_KEY, MINISTER_KEY, POPULATION_KEY, \
    GOVERNMENT_KEY,AREA_KEY, WHO_KEY, IS_KEY, THE_KEY, OF_KEY, WHAT_KEY, WHEN_KEY, WAS_KEY

from geq_queries import capital_of_country_query, area_of_country_query, government_of_country_query, \
    population_of_country_query, \
    president_of_country_query, prime_minister_of_country_query, prime_minister_born_date_query, \
    president_born_date_query, who_query


def get_last_argument(words):
    return ' '.join(words)[:-1]


def parse_who_is(words):
    question_number = None
    arg = None
    if len(words) > 5 and (words[3] == PRIME_KEY or words[3] == PRESIDENT_KEY):
        # can be i, ii
        if words[3] == PRESIDENT_KEY and words[4] == OF_KEY:
            question_number = 1
            arg = get_last_argument(words[5:])
        elif words[3] == PRIME_KEY and words[4] == MINISTER_KEY and words[5] == OF_KEY:
            question_number = 2
            arg = get_last_argument(words[6:])
    elif len(words) > 2:
        question_number = 9
        arg = get_last_argument(words[2:])
    return question_number, arg


def parse_what_is_the(words):
    question_number = None
    arg = None
    # can be iii, iv, v ,vi
    if words[3] == POPULATION_KEY:
        # iii
        question_number = 3
        arg = get_last_argument(words[5:])
    elif words[3] == AREA_KEY:
        # iv
        question_number = 4
        arg = get_last_argument(words[5:])
    elif words[3] == GOVERNMENT_KEY:
        question_number = 5
        arg = get_last_argument(words[5:])
        # v
    elif words[3] == CAPITAL_KEY:
        # vi
        question_number = 6
        arg = get_last_argument(words[5:])
    return question_number, arg


def parse_when_was_the(words):
    question_number = None
    arg = None
    # can be vii, viii
    if words[3] == PRESIDENT_KEY and words[4] == OF_KEY and words[len(words) - 1] == BORN_KEY:
        question_number = 7
        arg = get_last_argument(words[5:len(words) - 1])
        # can be vii
    elif words[3] == PRIME_KEY and words[4] == MINISTER_KEY and words[5] == OF_KEY and words[len(words) - 1] == BORN_KEY:
        question_number = 8
        arg = get_last_argument(words[6:len(words) - 1])
    return question_number, arg


def parse_user_question(string):
    question_number = None
    arg = None
    words = string.lower().split(" ")
    if len(words) == 0 or len(words) < 3 or words[len(words) - 1][-1] != '?':
        return question_number, arg
    if words[0] == WHO_KEY and words[1] == IS_KEY:
        # can be only i, ii, ix
        question_number, arg = parse_who_is(words)
    elif len(words) > 5 and words[0] == WHAT_KEY and words[1] == IS_KEY and words[2] == THE_KEY and words[4] == OF_KEY:
        question_number, arg = parse_what_is_the(words)
    elif len(words) > 6 and words[0] == WHEN_KEY and words[1] == WAS_KEY and words[2] == THE_KEY:
        question_number, arg = parse_when_was_the(words)
    return question_number, arg


def do_request(question, arg):
    ans = None
    if question == 1:
        print(president_of_country_query(arg))
    elif question == 2:
        print(prime_minister_of_country_query(arg))
    elif question == 3:
        print(population_of_country_query(arg))
    elif question == 4:
        print(area_of_country_query(arg))
    elif question == 5:
        print(government_of_country_query(arg))
    elif question == 6:
        print(capital_of_country_query(arg))
    elif question == 7:
        print(president_born_date_query(arg))
    elif question == 8:
        print(prime_minister_born_date_query(arg))
    elif question == 9:
        print(who_query(arg))
    else:
        print("ERROR")


def start_console(question):
    question, arg = parse_user_question(question)
    if question is None or arg is None:
        print('Invalid question, please enter new question.')
    else:
        do_request(question, arg)

