#! /usr/bin/python3.5

from console_interface.command_parser import *
from lib.task import TaskAttributes
from console_interface.interface import Interface
import console_interface.printers as printers
from console_interface.config_manager import ConfigManager
import datetime as dt


def main():
    parser = get_parser()
    command_dict = vars(parser.parse_args())
    command = command_dict.pop(ParserCommands.COMMAND)
    user = ConfigManager().get_default_user()
    if command == ParserObjects.USER:
        subcommand = command_dict[ParserCommands.SUBCOMMAND]
        if subcommand == UserCommandArguments.SET:
            ConfigManager().set_default_user(command_dict[UserCommandArguments.NAME])
            print("Hi, {}! Glad to see you!".format(command_dict[UserCommandArguments.NAME]))
            return 0

    if user is None:
        print("Hi, dear User. Please introduce yourself to py_tracker by calling 'py_tracker user set YOUR_NAME''.")
        return 0
    i = Interface(user)

    if command != ParserCommands.CHECK:
        subcommand = command_dict.pop(ParserCommands.SUBCOMMAND)
    else:
        subcommand = ParserCommands.CHECK
    try:
        if command == ParserObjects.TASK:
            if subcommand == ParserCommands.ADD:
                i.add_task(**command_dict)
            elif subcommand == ParserCommands.RM:
                try:
                    if command_dict[RemoveTaskCommandArguments.F]:
                        for k in command_dict[TaskAttributes.UID]:
                            i.remove_with_subtasks(k)
                    else:
                        for k in command_dict[TaskAttributes.UID]:
                            i.remove_task(k)
                except AttributeError:
                    print("! TASK: The task you're trying to delete has subtasks. Please remove them or use -f flag")

            elif subcommand == ParserCommands.FIND:
                tasks = list(i.find_tasks(**command_dict).values())
                for t in tasks:
                    printers.simple_task_printer(t)

            elif subcommand == ParserCommands.PRINT:
                if command_dict[PrintTaskCommandArguments.ID]:
                    task = i.get_task(command_dict[PrintTaskCommandArguments.ID])
                    printers.simple_task_printer(task, attributes=command_dict)
                else:
                    # todo: implement choise
                    tasks_d = i.tasks_manager.tasks
                    printers.hierarchy_printer(tasks_d)

            elif subcommand == ParserCommands.CHECK:
                if command_dict[CheckCommandArguments.DATE] is not None:
                    date = parse_date(command_dict[CheckCommandArguments.DATE])
                else:
                    date = dt.datetime.now()
                actual_tasks, reminders = i.check_time(date)
                for each in reminders:
                    printers.simple_reminder_printer(each)
                printers.simple_actual_tasks_printer(**actual_tasks)

        elif command == ParserObjects.PLAN:

            if subcommand == ParserCommands.ADD:
                period = command_dict[AddPlanCommandArguments.PERIOD]
                period = dt.timedelta(minutes=period)
                end_date = command_dict[AddPlanCommandArguments.FINISH]
                task_id = command_dict[AddPlanCommandArguments.TASK_ID]
                task_template = i.get_task(task_id)
                try:
                    i.add_periodic_plan(period, task_template, task_id, end_date)
                except PermissionError:
                    print("")
                i.check_plans()

            elif subcommand == ParserCommands.RM:
                for k in command_dict[RemovePlanCommandArguments.PLAN_ID]:
                    i.rm_periodic_plan(k)
        elif command == ParserObjects.USER:
            if subcommand == UserCommandArguments.GET:
                print('USERNAME: {}'.format(i.current_user))

    except PermissionError as e:
        print("! Py_Tracker: Permission denied for user: {}".format(i.current_user))
    except KeyError as e:
        print("! Py_Tracker: The key {} can't be found. Please check if it is correct".format(e.args))


if __name__ == '__main__':
    main()

