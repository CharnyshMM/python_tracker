from lib.task import TaskAttributes,TaskPriority,TaskStatus
import argparse
import uuid
import datetime as dt
import re


class ParserCommands:
    COMMAND = 'command'
    ADDTASK = 'addtask'
    RMTASK = 'rmtask'
    CHECK = 'check'
    FIND = 'find'
    ADDPLAN = 'addplan'
    PRINT = 'print'

class RemoveCommandArguments:
    ID = 'uid'
    F = 'f'

    @staticmethod
    def dash(arg):
        return '-' + arg

class CheckCommandArguments:
    DATE = 'date'
    ID = 'uid'


class FindCommandArguments:
    ID = 'uid'
    TITLE = 'title'

class PlanCommandArguments:
    TASK_ID = 'task_id'
    PERIOD = 'period'
    FINISH = 'finish'

class PrintCommandArguments:
    PRINT_DATES = 'print_dates'
    ID = 'id'
    PRINT_TAGS = 'print_tags'
    PRINT_USERS = 'print_users'
    PRINT_PLANS = 'print_plans'



def parse_date(date_str):
    try:
        if date_str is None:
            return None
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

def parse_period(period_str):
    try:
        return int(period_str)
    except Exception:
        raise argparse.ArgumentTypeError()

def get_parser():
    parser = argparse.ArgumentParser(prog='pytracker')
    subparsers = parser.add_subparsers(dest=ParserCommands.COMMAND, help='command help')
    addtask_parser = subparsers.add_parser(ParserCommands.ADDTASK, help='add task help')
    addtask_parser.add_argument(TaskAttributes.TITLE, type=str, help='title of task (required)')
    add_task_arguments(addtask_parser)

    rmtask_parser = subparsers.add_parser('rmtask', help='rmtask help')
    rmtask_parser.add_argument(dest=TaskAttributes.UID, type=parse_uuid, help="id of task to be removed")
    rmtask_parser.add_argument('-f', action='store_true', dest=RemoveCommandArguments.F, help='forse remove with subtasks')

    modtask_parser = subparsers.add_parser('modtask', help='modify task info')
    modtask_parser.add_argument(dest=TaskAttributes.UID,help='id of task to be modified')
    modtask_parser.add_argument('-title', type=str, dest=TaskAttributes.TITLE, help='title of task')
    add_task_arguments(modtask_parser)

    check_parser = subparsers.add_parser('check', help='check actual tasks')
    check_parser.add_argument('-d','--date', dest=CheckCommandArguments.DATE, type=parse_date, help='actual on date %d/%m/%y_%H:%M')

    print_parser = subparsers.add_parser('print', help='print task(s)')
    print_parser.add_argument('-id', type=parse_uuid)
    print_parser.add_argument('-d', '--dates', dest=PrintCommandArguments.PRINT_DATES, action='store_true')
    print_parser.add_argument('-t', '--tags', dest=PrintCommandArguments.PRINT_TAGS, action='store_true')
    print_parser.add_argument('-u', '--users', dest=PrintCommandArguments.PRINT_USERS, action='store_true')
    print_parser.add_argument('-p','--plans',dest=PrintCommandArguments.PRINT_PLANS, action='store_true')

    addplan_parser = subparsers.add_parser(ParserCommands.ADDPLAN, help='add plan help')
    addplan_parser.add_argument('period', type=parse_period)
    addplan_parser.add_argument('task_id', type=parse_uuid, help='task_id to template task that needs to become periodic')
    addplan_parser.add_argument('-finish', type=parse_date, default=None, help='when to finish plan')

    find_parser = subparsers.add_parser('find', help='find task by arguments')
    find_parser.add_argument('-t','--title', dest=FindCommandArguments.TITLE, help='find task by title')
    add_task_arguments(find_parser)

    return parser


def add_task_arguments(parser):
    parser.add_argument('-status', dest=TaskAttributes.STATUS, choices=[TaskStatus.ACTIVE,
                                                                        TaskStatus.COMPLITE,
                                                                        TaskStatus.ARCHIVED,
                                                                        TaskStatus.REJECTED], help='choise status attr')
    parser.add_argument('-starts',dest=TaskAttributes.START_DATE, type=parse_date, help='%d/%m/%y_%H:%M devide with slashes and semicolon')

    parser.add_argument('-remind', dest=TaskAttributes.REMIND_DATES, type=parse_date, nargs='*',help='%d/%m/%y_%H:%M devide with slashes and semicolon' )
    parser.add_argument('-ends', dest=TaskAttributes.END_DATE, type=parse_date, help='%d/%m/%y_%H:%M devide with slashes and semicolon')
    parser.add_argument('-parent',dest=TaskAttributes.OWNED_BY, type=parse_uuid, help='just ID')
    parser.add_argument('-subs', dest=TaskAttributes.SUBTASKS, type=parse_uuid, nargs='*',help='ids of subtasks')
    parser.add_argument('-tags', dest=TaskAttributes.TAGS, type=parse_date, nargs='*', help='any words you like')
    parser.add_argument('-editors', dest=TaskAttributes.CAN_EDIT, nargs='*', help='usernames of those who are able to edit this task')
