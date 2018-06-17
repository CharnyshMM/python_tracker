"""This module has a get_parser method to return a complete console input parser and commands collections"""

from lib.entities.task import TaskAttributes, TaskStatus
import argparse
import uuid
import datetime as dt


class ParserCommands:

    COMMAND = 'command'
    SUBCOMMAND = 'subcommand'

class TaskCommands:
    """Commands that can be called to operate with tasks."""
    TASK = 'task'
    class AddSubcommand:
        ADD = 'add'
    class PrintSubcommand:
        PRINT = 'print'
        WIDE = 'w'
        ID = 'id'  #change
        SUBTASKS = 's'

    class RemoveSubcommand:
        RM = 'rm'
        ID = 'uid'
        F = 'f'
    class EditSubcommand:
        EDIT = 'edit'
        EDIT_KIND = 'edit_kind'
        ADD = 'add'
        RM = 'rm'
        SET = 'set'
        UNSET = 'unset'
        ID = 'id'

    class FindSubcommand:
        FIND = 'find'
        ID = 'uid'
        TITLE = 'title'
    class CompleteSubcommand:
        COMPLETE = 'complete'

class PlanCommands:
    """Commands that can be called to operate with plans"""
    PLAN = 'plan'

    class AddSubcommand:
        ADD = 'add'
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

    class RemoveSubcommand:
        RM = 'rm'
        PLAN_ID = 'id'

    class PrintSubcommand:
        PRINT = 'print'
        ID = 'uid'

class UserCommands:
    USER = 'user'
    SET = 'set'
    GET = 'get'
    NAME = 'name'

class CheckCommand:
    CHECK = 'check'
    PRIORITY = 'priority'
    STATUS = 'status'
    ID = 'uid'

class ParserObjects:
    TASK = 'task'
    PLAN = 'plan'
    USER = 'user'


def valid_date(date_str):
    try:
        if date_str is None:
            return None

        if date_str == 'now':
            time_now = dt.datetime.now()
            return dt.datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=time_now.hour,
                               minute=time_now.minute)

        return dt.datetime.strptime(date_str, "%d/%m/%y %H:%M")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date_str)
        raise argparse.ArgumentTypeError(msg)


def valid_uuid(uuid_str):
    try:
        return uuid.UUID(uuid_str)
    except ValueError:
        msg = "Not a valid ID '{}'".format(uuid_str)
        raise argparse.ArgumentTypeError(msg)


def parse_period(command_dict):
    """Parse plan period input"""

    if command_dict[PlanCommands.AddSubcommand.FIXED] is not None:
        return command_dict[PlanCommands.AddSubcommand.FIXED]
    if command_dict[PlanCommands.AddSubcommand.DAYS] is not None:
        return dt.timedelta(days=command_dict[PlanCommands.AddSubcommand.DAYS])
    if command_dict[PlanCommands.AddSubcommand.HOURS] is not None:
        return dt.timedelta(hours=command_dict[PlanCommands.AddSubcommand.HOURS])
    if command_dict[PlanCommands.AddSubcommand.MINS] is not None:
        return dt.timedelta(minutes=command_dict[PlanCommands.AddSubcommand.MINS])


def valid_positive(val):
    val = int(val)
    if not isinstance(val,int) or val <= 0:
        raise argparse.ArgumentTypeError('Not a valid value {}'.format(val))
    return val


def get_parser():
    parser = argparse.ArgumentParser(prog='py_tracker')
    object_subparsers = parser.add_subparsers(dest='command',help='console interface for task tracker. '
                                                                  'Add, remove and plan tasks with it ;)')
    # OBJECT COMMANDS
    user_parser = object_subparsers.add_parser(UserCommands.USER, help='introduce yourself to py_tracker')
    task_parser = object_subparsers.add_parser(TaskCommands.TASK, help='to manage task objects')
    plan_parser = object_subparsers.add_parser(PlanCommands.PLAN, help='to manage plan objects')

    # CHECK COMMAND
    check_parser = object_subparsers.add_parser(CheckCommand.CHECK, help='check actual tasks')
    check_parser.add_argument('-s','--status', dest=CheckCommand.STATUS,
                              choices=[TaskStatus.ACTIVE,
                                       TaskStatus.COMPLETE],
                              help='tasks with only selected status would be shown if specified')
    check_parser.add_argument('-p','--priority',
                              choices=[1,2,3],
                              type=int,
                              dest=CheckCommand.PRIORITY,
                              help='lest priority to be shown.  (1,2,3. 1 is the highest)')

    # USER SET & GET
    user_subparser = user_parser.add_subparsers(dest=ParserCommands.SUBCOMMAND)
    set_user_parser = user_subparser.add_parser(UserCommands.SET, help='log in and interact as USER')
    set_user_parser.add_argument(UserCommands.NAME, help='Your username')
    user_subparser.add_parser(UserCommands.GET,help='show your username')

    task_subparsers = task_parser.add_subparsers(dest=ParserCommands.SUBCOMMAND)

    # TASK ADD
    add_task_parser = task_subparsers.add_parser(TaskCommands.AddSubcommand.ADD, help='add new task')
    add_task_parser.add_argument(TaskAttributes.TITLE,  help='title of a new task')
    add_task_optional_attributes(add_task_parser)

    # TASK EDIT
    edit_task_parser = task_subparsers.add_parser(TaskCommands.EditSubcommand.EDIT, help='edit some attributes of existing task')
    edit_task_parser.add_argument(TaskCommands.EditSubcommand.ID,type=valid_uuid, help='id of task to be edited')
    edit_task_subparsers = edit_task_parser.add_subparsers(dest=TaskCommands.EditSubcommand.EDIT_KIND, help='set,add, remove')
    set_edit_parser = edit_task_subparsers.add_parser(TaskCommands.EditSubcommand.SET, help='set title, status, priority, time')
    unset_edit_parser = edit_task_subparsers.add_parser(TaskCommands.EditSubcommand.UNSET,help='unset start or end time attribute')
    add_edit_parser = edit_task_subparsers.add_parser(TaskCommands.EditSubcommand.ADD,help='add reminder, users, tags')
    rm_edit_parser = edit_task_subparsers.add_parser(TaskCommands.EditSubcommand.RM, help='remove reminder,users, tags')
    # TASK EDIT SET
    set_group = set_edit_parser.add_mutually_exclusive_group(required=True)
    set_group.add_argument('--status', dest=TaskAttributes.STATUS,
                           choices=[TaskStatus.ACTIVE,
                                    TaskStatus.COMPLETE],
                           type=str,
                           help='choose new status value')
    set_group.add_argument('--priority', dest=TaskAttributes.PRIORITY,
                           choices=[1,2,3],
                           type=int,
                           help='choose new priority. (1,2,3. 1 is the highest)')
    set_group.add_argument('--title',dest=TaskAttributes.TITLE,help='new title')
    set_group.add_argument('--starts', dest=TaskAttributes.START_TIME, type=valid_date,
                           help='"dd/mm/yy hh:mm", separate with slashes and semicolon, or "now"')
    set_group.add_argument('--ends', dest=TaskAttributes.END_TIME, type=valid_date,
                           help='"dd/mm/yy hh:mm", separate with slashes and semicolon or "now"')

    # TASK EDIT UNSET
    unset_group = unset_edit_parser.add_mutually_exclusive_group(required=True)
    unset_group.add_argument('--start', dest=TaskAttributes.START_TIME, action='store_true',
                             help="unset task start time. It'll be treated than like started already")
    unset_group.add_argument('--end', dest=TaskAttributes.END_TIME, action='store_true',
                             help="unset task end time. It'll be treated than like never ending")

    # TASK EDIT ADD
    add_group = add_edit_parser.add_mutually_exclusive_group(required=True)
    add_edit_group_arguments(add_group)

    # TASK EDIT RM
    add_edit_group_arguments(rm_edit_parser.add_mutually_exclusive_group(required=True))

    # TASK COMPLETE
    complete_parser = task_subparsers.add_parser('complete', help='change task status to COMPLETE')
    complete_parser.add_argument(TaskAttributes.UID, type=valid_uuid, help='ID of completed task')

    # TASK RM
    rm_task_parser = task_subparsers.add_parser('rm',help='remove a task')
    rm_task_parser.add_argument(TaskAttributes.UID, nargs='+', type=valid_uuid, help='ID of task to be removed')
    rm_task_parser.add_argument('-f', action='store_true', dest=TaskCommands.RemoveSubcommand.F, help='remove task with its subtasks')

    # TASK PRINT
    print_task_parser = task_subparsers.add_parser('print', help='simply print task(s)')
    print_single_task_group = print_task_parser.add_argument_group('additional single task print options')

    print_single_task_group.add_argument('-id',
                                   type=valid_uuid,
                                   dest=TaskCommands.PrintSubcommand.ID,
                                   help='print only the task with this ID')
    print_single_task_group.add_argument('-s', '--subs',
                                         dest=TaskCommands.PrintSubcommand.SUBTASKS,
                                         action='store_true', help='print task with subtasks')

    print_task_parser.add_argument('-w','--wide',
                                   dest=TaskCommands.PrintSubcommand.WIDE,
                                   action='store_true', help='print whole the info about a task')

    # TASK FIND
    find_parser = task_subparsers.add_parser(TaskCommands.FindSubcommand.FIND, help='find task by arguments')
    find_parser.add_argument('-t', '--title', dest=TaskAttributes.TITLE, help='find task by title')
    add_task_optional_attributes(find_parser)

    plan_subparsers = plan_parser.add_subparsers(dest=ParserCommands.SUBCOMMAND)

    # PLAN ADD
    add_plan_parser = plan_subparsers.add_parser(PlanCommands.AddSubcommand.ADD,
                                                 help='new periodic plan for existing task')
    fixed_period_group = add_plan_parser.add_mutually_exclusive_group(required=True)
    fixed_period_group.add_argument('--fixed', dest=PlanCommands.AddSubcommand.FIXED,
                                    choices=['yearly','monthly','weekly','daily'],help='fixed period')
    fixed_period_group.add_argument('--days', dest=PlanCommands.AddSubcommand.DAYS, type=valid_positive, help='every N days')
    fixed_period_group.add_argument('--hours', dest=PlanCommands.AddSubcommand.HOURS, type=valid_positive, help='every N hours')
    fixed_period_group.add_argument('--mins',dest=PlanCommands.AddSubcommand.MINS, type=valid_positive, help='every N minutes')

    add_plan_parser.add_argument(PlanCommands.AddSubcommand.TASK_ID, type=valid_uuid, help='task_id to template task for the plan')
    add_plan_parser.add_argument('--finish',
                                 dest=PlanCommands.AddSubcommand.FINISH,
                                 type=valid_date, default=None,
                                 help='when to finish repeating')

    # PLAN RM
    rm_plan_parser = plan_subparsers.add_parser('rm',help='remove plan by ID')
    rm_plan_parser.add_argument('id', nargs='+', type=valid_uuid, help='plans id')

    # PLAN PRINT
    print_plan_parser = plan_subparsers.add_parser('print', help='print all the plans')
    print_plan_parser.add_argument('-id', dest=PlanCommands.PrintSubcommand.ID, type=valid_uuid, help='print single plan by ID')

    return parser


def add_task_optional_attributes(parser):
    """Adds optional Task Attribute arguments to a given parser"""
    parser.add_argument('--status', dest=TaskAttributes.STATUS,
                        choices=[TaskStatus.ACTIVE,
                                 TaskStatus.COMPLETE],
                        help='choose status value')
    parser.add_argument('--priority', dest=TaskAttributes.PRIORITY,
                        choices=[1, 2, 3],
                        type=int,
                        help='task priority (1,2,3. 1 is the highest)')
    parser.add_argument('--starts', dest=TaskAttributes.START_TIME, type=valid_date,
                        help='"dd/mm/yy hh:mm", separate with slashes and semicolon or just type "now"')
    parser.add_argument('--remind', dest=TaskAttributes.REMIND_TIMES, type=valid_date, nargs='*',
                        help='"dd/mm/yy hh:mm", separate with slashes and semicolon or just type "now"')
    parser.add_argument('--ends', dest=TaskAttributes.END_TIME, type=valid_date,
                        help=r'"dd/mm/yy_hh:mm", separate with slashes and semicolon or just type "now"')
    parser.add_argument('--parent', dest=TaskAttributes.PARENT, type=valid_uuid, help='just ID')
    parser.add_argument('--subs', dest=TaskAttributes.SUBTASKS, type=valid_uuid, nargs='*', help='ids of subtasks')
    parser.add_argument('--tags', dest=TaskAttributes.TAGS, type=str, nargs='*', help='any words you like')
    parser.add_argument('--editors', dest=TaskAttributes.CAN_EDIT, type=str, nargs='*',
                        help='usernames of those who are able to edit this task')


def add_edit_group_arguments(group):
    """Adds user, reminder and tag arguments to a given task edit parser group"""

    group.add_argument('--user', dest=TaskAttributes.CAN_EDIT,help='user who can edit the task')
    group.add_argument('--reminder', type=valid_date, dest=TaskAttributes.REMIND_TIMES,
                       help='reminder time, "dd/mm/yy_hh:mm" devide with slashes and semicolon')
    group.add_argument('--tag', dest=TaskAttributes.TAGS,help='tag')