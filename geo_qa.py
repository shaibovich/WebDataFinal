import sys
from const import CREATE_ONTOLOGY, QUESTION_ONTOLOGY, FILE_NAME
from geo_console import start_console
from geo_ontology import start


def validate_command_line_args(args):
    if len(args) < 2:
        raise Exception("Invalid program commands.")
    if args[1] != CREATE_ONTOLOGY and args[1] != QUESTION_ONTOLOGY:
        raise Exception("Invalid program commands. Wrong command, command is {}".format(args[2]))
    if args[1] == CREATE_ONTOLOGY and args[2] != FILE_NAME:
        raise Exception("Invalid program commands. Wrong file name")


def do_command(arg, param):
    if arg == CREATE_ONTOLOGY:
        start(FILE_NAME)
    elif arg == QUESTION_ONTOLOGY:
        start_console(param)


validate_command_line_args(sys.argv)
arg = sys.argv[1]
param = sys.argv[2]
do_command(arg, param)
