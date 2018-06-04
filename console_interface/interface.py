
from .my_parser import *
from lib.task import TaskAttributes, TaskStatus,TaskPriority,TaskPlanAttributes
from lib.interface import Interface
import console_interface.printers as printers
import uuid


def main():
    parser = get_parser()
    i = Interface("mikita") # todo: CHANGE THISTHTHT
    command_dict = vars(parser.parse_args())
    command = command_dict.pop(ParserCommands.COMMAND)
    if command == ParserCommands.ADDTASK:
        i.add_task(**command_dict)
    elif command == ParserCommands.RMTASK:
        id_str = command_dict[TaskAttributes.UID].replace('"','')
        id_str = id_str.replace("'",'')
        i.remove_task(uuid.UUID(id_str))
    elif command == ParserCommands.PRINT:
        tasks = i.get_all_tasks()
        for t in tasks:
            printers.simple_task_printer(t)


if __name__ == '__main__':
    main()

