#! /usr/bin/python3.5

from console_interface.my_parser import *
from lib.task import TaskAttributes, TaskStatus,TaskPriority,TaskPlanAttributes
from lib.interface import Interface
import console_interface.printers as printers
import uuid
import datetime as dt


def main(args):
    parser = get_parser()
    i = Interface("mikita") # todo: CHANGE THISTHTHT
    command_dict = vars(parser.parse_args(args.split(" ")))
    command = command_dict.pop(ParserCommands.COMMAND)
    if command == ParserCommands.ADDTASK:
        try:
            i.add_task(**command_dict)
        except PermissionError as e:
            print(print("! ADDTASK: Permission denied for user: {}".format(i.current_user)))

    elif command == ParserCommands.RMTASK:
        try:
            if command_dict[RemoveCommandArguments.F]:
                i.remove_with_subtasks(command_dict[TaskAttributes.UID])
            else:
                i.remove_task(command_dict[TaskAttributes.UID])
        except AttributeError:
            print("! RMTASK: The task you're trying to delete has subtasks. Please remove them or use -f flag")
        except PermissionError:
            print("! RMTASK: Permission denied for user: {}".format(i.current_user))

    elif command == ParserCommands.FIND:
        tasks = list(i.find_tasks(**command_dict).values())
        for t in tasks:
            printers.simple_task_printer(t)
    elif command == ParserCommands.CHECK:
        if command_dict[CheckCommandArguments.DATE] is not None:
            date = parse_date(command_dict[CheckCommandArguments.DATE])
        else:
            date = dt.datetime.now()
        actual_tasks, reminders = i.check_time(date)
        for each in reminders:
            printers.simple_reminder_printer(each)

        printers.simple_actual_tasks_printer(**actual_tasks)

if __name__ == '__main__':
    main(input())

