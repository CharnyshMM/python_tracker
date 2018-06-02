import lib.interface
import argparse

def get_parser():
    parser = argparse.ArgumentParser(prog='pytracker')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "a" command
    addtask_parser = subparsers.add_parser('addtask', help='add task help')
    addtask_parser.add_argument('-name', type=str, required=True, help='name help')
    add_task_arguments(addtask_parser)
    # create the parser for the "b" command
    rmtask_parser = subparsers.add_parser('rmtask', help='rmtask help')
    rmtask_parser.add_argument('-f', action='store_true', help='complitety remove help')

    modtask_parser = subparsers.add_parser('modtask',help='modtask help')
    modtask_parser.add_argument('-name', type=str, help='name help')
    add_task_arguments(modtask_parser)

    check_parser = subparsers.add_parser('check')
    check_parser.add_argument('-d','--date',help='help date')

    return parser

def add_task_arguments(parser):
    parser.add_argument('-starts')
    parser.add_argument('-remind', nargs='*')
    parser.add_argument('-ends')
    parser.add_argument('-in')
    parser.add_argument('-subs', nargs='*')
    parser.add_argument('-tags', nargs='*')
    parser.add_argument('-editors', nargs='*')