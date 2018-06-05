
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
        normalise_result_dict(command_dict)
        i.add_task(**command_dict)
    elif command == ParserCommands.RMTASK:
        id_str = command_dict[TaskAttributes.UID].replace('"', '')
        id_str = id_str.replace("'",'')
        i.remove_task(uuid.UUID(id_str))
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

