from lib.task import TaskAttributes,TaskPriority,TaskPlanAttributes,TaskStatus
import argparse


class ParserCommands:
    COMMAND = 'command'
    ADDTASK = 'addtask'
    RMTASK = 'rmtask'
    CHECK = 'check'
    PRINT = 'print'



class RemoveCommandArguments:
    ID = 'id'
    F = 'f'

    @staticmethod
    def dash(arg):
        return '-' + arg

class CheckCommandArguments:
    DATE = 'date'
    ID = 'id'


class PrintCommandArguements:
    ID = 'id'
    TITLE = 'title'



def get_parser():
    parser = argparse.ArgumentParser(prog='pytracker')
    subparsers = parser.add_subparsers(dest=ParserCommands.COMMAND, help='command help')
    addtask_parser = subparsers.add_parser(ParserCommands.ADDTASK, help='add task help')
    addtask_parser.add_argument(TaskAttributes.TITLE, type=str, help='title of task (required)')
    add_task_arguments(addtask_parser)

    rmtask_parser = subparsers.add_parser(ParserCommands.RMTASK, help='rmtask help')
    rmtask_parser.add_argument(dest=TaskAttributes.UID, help="id of task to be removed")
    rmtask_parser.add_argument('-f', action='store_true',dest=RemoveCommandArguments.F, help='forse remove with subtasks')

    modtask_parser = subparsers.add_parser('modtask', help='modify task info')
    modtask_parser.add_argument(dest=TaskAttributes.UID,help='id of task to be modified')
    modtask_parser.add_argument('-title', type=str, dest=TaskAttributes.TITLE, help='title of task')
    add_task_arguments(modtask_parser)

    check_parser = subparsers.add_parser('check')
    check_parser.add_argument('-d','--date', dest=CheckCommandArguments.DATE, help='since date')

    print_parser = subparsers.add_parser('print')
    print_parser.add_argument('-id',dest=PrintCommandArguements.ID, help='print task by id') # todo: сделать чтобы только один вариант был
    print_parser.add_argument('-t','--title', dest=PrintCommandArguements.TITLE,help='find task by title')

    return parser


def add_task_arguments(parser):
    parser.add_argument('-status', dest=TaskAttributes.STATUS, choices=[TaskStatus.ACTIVE,
                                                                        TaskStatus.COMPLITE,
                                                                        TaskStatus.ARCHIVED,
                                                                        TaskStatus.REJECTED])
    parser.add_argument('-remind', dest=TaskAttributes.REMIND_DATES, nargs='*')
    parser.add_argument('-ends', dest=TaskAttributes.END_DATE)
    parser.add_argument('-parent',dest=TaskAttributes.OWNED_BY)
    parser.add_argument('-subs', dest=TaskAttributes.SUBTASKS, nargs='*')
    parser.add_argument('-tags', dest=TaskAttributes.TAGS, nargs='*')
    parser.add_argument('-editors', dest=TaskAttributes.CAN_EDIT, nargs='*')






