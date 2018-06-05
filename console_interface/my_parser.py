from lib.task import TaskAttributes,TaskPriority,TaskPlanAttributes,TaskStatus
import argparse
import uuid
import datetime as dt


class ParserCommands:
    COMMAND = 'command'
    ADDTASK = 'addtask'
    RMTASK = 'rmtask'
    CHECK = 'check'
    FIND = 'find'

class RemoveCommandArguments:
    ID = 'uid'
    F = 'f'

    @staticmethod
    def dash(arg):
        return '-' + arg

class CheckCommandArguments:
    DATE = 'date'
    ID = 'uid'


class FindCommandArguements:
    ID = 'uid'
    TITLE = 'title'


def parse_date(date_str):
    try:
        return dt.datetime.strptime(date_str, "%d/%m/%y_%H:%M")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date_str)
        raise argparse.ArgumentTypeError(msg)

def parse_uuid(uuid_str):
    try:
        return uuid.UUID(uuid_str)
    except ValueError:
        msg = "Not a valid ID '{}'".format(uuid_str)
        raise argparse.ArgumentTypeError(msg)


def get_parser():
    parser = argparse.ArgumentParser(prog='pytracker')
    subparsers = parser.add_subparsers(dest=ParserCommands.COMMAND, help='command help')
    addtask_parser = subparsers.add_parser(ParserCommands.ADDTASK, help='add task help')
    addtask_parser.add_argument(TaskAttributes.TITLE, type=str, help='title of task (required)')
    add_task_arguments(addtask_parser)

    rmtask_parser = subparsers.add_parser(ParserCommands.RMTASK, help='rmtask help')
    rmtask_parser.add_argument(dest=TaskAttributes.UID, type=parse_uuid, help="id of task to be removed")
    rmtask_parser.add_argument('-f', action='store_true', dest=RemoveCommandArguments.F, help='forse remove with subtasks')

    modtask_parser = subparsers.add_parser('modtask', help='modify task info')
    modtask_parser.add_argument(dest=TaskAttributes.UID,help='id of task to be modified')
    modtask_parser.add_argument('-title', type=str, dest=TaskAttributes.TITLE, help='title of task')
    add_task_arguments(modtask_parser)

    check_parser = subparsers.add_parser('check')
    check_parser.add_argument('-d','--date', dest=CheckCommandArguments.DATE, help='since date')

    subparsers.add_parser('hier')

    print_parser = subparsers.add_parser('find')
    # print_parser.add_argument(dest=PrintCommandArguements.ID, help='print task by id')
    #  todo: сделать чтобы только один вариант был
    print_parser.add_argument('-t','--title', dest=FindCommandArguements.TITLE, help='find task by title')
    add_task_arguments(print_parser)
    return parser


def add_task_arguments(parser):
    parser.add_argument('-status', dest=TaskAttributes.STATUS, choices=[TaskStatus.ACTIVE,
                                                                        TaskStatus.COMPLITE,
                                                                        TaskStatus.ARCHIVED,
                                                                        TaskStatus.REJECTED])
    parser.add_argument('-starts',dest=TaskAttributes.START_DATE, type=parse_date, help='%d/%m/%y_%H:%M devide with slashes and semicolon')

    parser.add_argument('-remind', dest=TaskAttributes.REMIND_DATES, type=parse_date, nargs='*')
    parser.add_argument('-ends', dest=TaskAttributes.END_DATE, type=parse_date)
    parser.add_argument('-parent',dest=TaskAttributes.OWNED_BY, type=parse_uuid)
    parser.add_argument('-subs', dest=TaskAttributes.SUBTASKS, type=parse_uuid, nargs='*')
    parser.add_argument('-tags', dest=TaskAttributes.TAGS, type=parse_date, nargs='*')
    parser.add_argument('-editors', dest=TaskAttributes.CAN_EDIT, nargs='*')
