from lib.task import TaskAttributes,TaskPriority,TaskStatus
import argparse
import uuid
import datetime as dt
from lib.plan import PeriodicPlanAttributes


class ParserCommands:
    #COMMAND = 'command'
    COMMAND = 'command'
    SUBCOMMAND = 'subcommand'
    ADD = 'add'
    RM = 'rm'
    SET = 'set'
    CHECK = 'check'
    FIND = 'find'
    PRINT = 'print'
    EDIT = 'edit'

class ParserObjects:
    TASK = 'task'
    PLAN = 'plan'
    USER = 'user'

class UserCommandArguments:
    SET = 'set'
    GET = 'get'
    NAME = 'name'

class RemoveTaskCommandArguments:
    ID = 'uid'
    F = 'f'

    @staticmethod
    def dash(arg):
        return '-' + arg

class CheckCommandArguments:
    DATE = 'date'
    ID = 'uid'


class FindTaskCommandArguments:
    ID = 'uid'
    TITLE = 'title'

class AddPlanCommandArguments:
    TASK_ID = 'task_id'
    FIXED = 'fixed'
    YEARLY = 'yearly'
    MONTHLY = 'monthly'
    WEEKLY = 'weekly'
    DAILY = 'daily'
    HOURS = 'hours'
    MINS = 'mins'
    DAYS = 'days'
    FINISH = 'finish'

class RemovePlanCommandArguments:
    PLAN_ID = 'id'
    REMOVE_WITH_TASKS = 'r'


class PrintTaskCommandArguments:
    PRINT_DATES = 'print_dates'
    ID = 'id'
    PRINT_TAGS = 'print_tags'
    PRINT_USERS = 'print_users'
    PRINT_PLAN = 'print_plan'
    HIERARCHY = 'hierarchy'

class TaskEditCommand:
    EDIT = 'edit'
    EDIT_KIND = 'edit_kind'
    ADD = 'add'
    RM = 'rm'
    SET = 'set'
    ID = 'id'



def valid_date(date_str):
    try:
        if date_str is None:
            return None
        return dt.datetime.strptime(date_str, "%d/%m/%y_%H:%M")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date_str)
        raise argparse.ArgumentTypeError(msg)

def valid_uuid(uuid_str):
    try:
        return uuid.UUID(uuid_str)
    except ValueError:
        msg = "Not a valid ID '{}'".format(uuid_str)
        raise argparse.ArgumentTypeError(msg)

def parse_priority(string):
    if string == 'high':
        return TaskPriority.HIGH
    if string == 'medium':
        return TaskPriority.MEDIUM
    if string == 'low':
        return TaskPriority.LOW


def parse_period(command_dict):
    if command_dict[AddPlanCommandArguments.FIXED] is not None:
        return command_dict[AddPlanCommandArguments.FIXED]
    if command_dict[AddPlanCommandArguments.DAYS] is not None:
        return dt.timedelta(days=command_dict[AddPlanCommandArguments.DAYS])
    if command_dict[AddPlanCommandArguments.HOURS] is not None:
        return dt.timedelta(hours=command_dict[AddPlanCommandArguments.HOURS])
    if command_dict[AddPlanCommandArguments.MINS] is not None:
        return dt.timedelta(minutes=command_dict[AddPlanCommandArguments.MINS])


def valid_positive(val):
    if not isinstance(val,int) or val <= 0:
        raise argparse.ArgumentTypeError('Not a valid value {}'.format(val))
    return val


def get_parser():
    parser = argparse.ArgumentParser(prog='py_tracker')
    object_subparsers = parser.add_subparsers(dest='command',help='console interface for task tracker. '
                                                                  'Add, remove and plan tasks with it ;)')
    # OBJECT COMMANDS
    user_parser = object_subparsers.add_parser('user', help='introduce yourself to py_tracker')
    task_parser = object_subparsers.add_parser('task', help='to manage task objects')
    plan_parser = object_subparsers.add_parser('plan', help='to manage plan objects')

    # CHECK COMMAND
    check_parser = object_subparsers.add_parser('check', help='check actual tasks')
    check_parser.add_argument('-d','--date', type=valid_date, help='check actual tasks on some date & time')

    # USER PARSER
    user_subparser = user_parser.add_subparsers(dest=ParserCommands.SUBCOMMAND)
    set_user_parser = user_subparser.add_parser('set', help='log in and interact as USER')
    set_user_parser.add_argument('name', help='Your username')
    user_subparser.add_parser('get',help='show your username')

    task_subparsers = task_parser.add_subparsers(dest=ParserCommands.SUBCOMMAND)

    # ADD TASK PARSER
    add_task_parser = task_subparsers.add_parser('add', help='add new task')
    add_task_parser.add_argument('title',  help='title of a new task')
    add_task_optional_attributes(add_task_parser)

    # EDIT TASK PARSER
    edit_task_parser = task_subparsers.add_parser('edit',help='edit some attributes of existing task')
    edit_task_parser.add_argument('id',type=valid_uuid, help='id of task to be edited')
    edit_task_subparsers = edit_task_parser.add_subparsers(dest=TaskEditCommand.EDIT_KIND, help='set,add, remove')
    set_edit_parser = edit_task_subparsers.add_parser('set', help='set title, status, priority, time')
    add_edit_parser = edit_task_subparsers.add_parser('add',help='add reminder, users, tags')
    rm_edit_parser = edit_task_subparsers.add_parser('rm', help='remove reminder,users, tags')
    # EDIT SET
    set_group = set_edit_parser.add_mutually_exclusive_group(required=True)
    set_group.add_argument('-status',dest=TaskAttributes.STATUS,
                           choices=[TaskStatus.ACTIVE,
                                    TaskStatus.COMPLITE,
                                    TaskStatus.ARCHIVED,
                                    TaskStatus.REJECTED],
                           help='choose new status value')
    set_group.add_argument('-priority', dest=TaskAttributes.PRIORITY,
                           choices=['high', 'medium', 'low'],
                           help='choose new priority')
    set_group.add_argument('-title',dest=TaskAttributes.TITLE,help='new title')

    # EDIT ADD
    add_group = add_edit_parser.add_mutually_exclusive_group(required=True)
    add_edit_group_arguments(add_group)

    add_edit_group_arguments(rm_edit_parser.add_mutually_exclusive_group(required=True))


    # RM TASK PARSER
    rm_task_parser = task_subparsers.add_parser('rm',help='remove a task')
    rm_task_parser.add_argument('uid', nargs='+', type=valid_uuid, help='ID of task to be removed')
    rm_task_parser.add_argument('-f', action='store_true', dest=RemoveTaskCommandArguments.F, help='remove task with its subtasks')

    # PRINT TASK PARSER
    print_task_parser = task_subparsers.add_parser('print', help='simply print task(s) with wider info')
    print_task_parser.add_argument('-id',
                                   type=valid_uuid,
                                   help='print only the task with this ID')
    print_task_parser.add_argument('-d','--dates',
                                   dest=PrintTaskCommandArguments.PRINT_DATES,
                                   action='store_true', help='print task dates')
    print_task_parser.add_argument('-t', '--tags',
                                   dest=PrintTaskCommandArguments.PRINT_TAGS,
                                   action='store_true')
    print_task_parser.add_argument('-u', '--users',
                                   dest=PrintTaskCommandArguments.PRINT_USERS,
                                   action='store_true', help='print users connected')
    print_task_parser.add_argument('-pl', '--plan',
                                   dest=PrintTaskCommandArguments.PRINT_PLAN,
                                   action='store_true', help='print plan id')
    print_task_parser.add_argument('-hr', '--hierarchy',
                                   dest=PrintTaskCommandArguments.HIERARCHY,
                                   action='store_true', help='hierarchical order')

    # FIND TASK
    find_parser = task_subparsers.add_parser('find', help='find task by arguments')
    find_parser.add_argument('-t', '--title',
                             dest=FindTaskCommandArguments.TITLE,
                             help='find task by title')

    plan_subparsers = plan_parser.add_subparsers(dest=ParserCommands.SUBCOMMAND)

    # ADD PLAN
    add_plan_parser = plan_subparsers.add_parser('add',
                                                 help='new periodic plan for existing task')

    fixed_period_group = add_plan_parser.add_mutually_exclusive_group(required=True)
    fixed_period_group.add_argument('-fixed',choices=['yearly','monthly','weekly','daily'],help='fixed period')
    fixed_period_group.add_argument('-days', type=valid_positive, help='every N days')
    fixed_period_group.add_argument('-hours', type=valid_positive, help='every N hours')
    fixed_period_group.add_argument('-mins', type=valid_positive, help='every N minutes')

    add_plan_parser.add_argument('task_id',
                                 type=valid_uuid,
                                 help='task_id to template task for the plan')
    add_plan_parser.add_argument('-finish',
                                 type=valid_date, default=None,
                                 help='when to finish repeating')

    # RM PLAN
    rm_plan_parser = plan_subparsers.add_parser('rm',help='remove plan by ID')
    rm_plan_parser.add_argument('id', nargs='+', type=valid_uuid, help='plans id')

    return parser


def add_task_optional_attributes(parser):
    parser.add_argument('-status', dest=TaskAttributes.STATUS,
                        choices=[TaskStatus.ACTIVE,
                                 TaskStatus.COMPLITE,
                                 TaskStatus.ARCHIVED,
                                 TaskStatus.REJECTED],
                        default=TaskStatus.ACTIVE,
                        help='choose status value')
    parser.add_argument('-priority',dest=TaskAttributes.PRIORITY,
                        choices=['high','medium','low'],
                        default='medium',
                        help='task priority')
    parser.add_argument('-starts', dest=TaskAttributes.START_DATE, type=valid_date,
                        help=r'"dd/mm/yy hh:mm" devide with slashes and semicolon')
    parser.add_argument('-remind', dest=TaskAttributes.REMIND_DATES, type=valid_date, nargs='*',
                        help=r'"dd/mm/yy hh:mm" devide with slashes and semicolon')
    parser.add_argument('-ends', dest=TaskAttributes.END_DATE, type=valid_date,
                        help=r'"dd/mm/yy_hh:mm" devide with slashes and semicolon')
    parser.add_argument('-parent', dest=TaskAttributes.OWNED_BY, type=valid_uuid, help='just ID')
    parser.add_argument('-subs', dest=TaskAttributes.SUBTASKS, type=valid_uuid, nargs='*', help='ids of subtasks')
    parser.add_argument('-tags', dest=TaskAttributes.TAGS, type=str, nargs='*', help='any words you like')
    parser.add_argument('-editors', dest=TaskAttributes.CAN_EDIT, type=str, nargs='*',
                        help='usernames of those who are able to edit this task')


def add_edit_group_arguments(group):
    group.add_argument('-user', dest=TaskAttributes.CAN_EDIT,help='user who can edit the task')
    group.add_argument('-reminder', type=valid_date, dest=TaskAttributes.REMIND_DATES,help='reminder time,'
                                                                                          ' "dd/mm/yy_hh:mm" devide with slashes and semicolon')
    group.add_argument('-tag', dest=TaskAttributes.TAGS,help='tag')