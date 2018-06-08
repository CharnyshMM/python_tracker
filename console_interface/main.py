#! /usr/bin/python3.5

from console_interface.command_parser import *
from lib.task import TaskAttributes
from console_interface.task_interface import Interface
import console_interface.printers as printers
from console_interface.config_manager import ConfigManager
from lib.exceptions import EndTimeOverflowError, SubtasksNotRemovedError, NoTimeValueError
import datetime as dt


def main():
    parser = get_parser()
    command_dict = vars(parser.parse_args())
    command = command_dict.pop(ParserCommands.COMMAND)
    user = ConfigManager().get_default_user()
    if command == ParserObjects.USER:
        subcommand = command_dict[ParserCommands.SUBCOMMAND]
        if subcommand == UserCommands.SET:
            ConfigManager().set_default_user(command_dict[UserCommands.NAME])
            print("Hi, {}! Glad to see you!".format(command_dict[UserCommands.NAME]))
            return 0

    if user is None:
        print("Hi, dear User. Please introduce yourself to py_tracker by calling 'py_tracker user set YOUR_NAME''.")
        return 0
    inteface = Interface(user)

    subcommand = None
    if command != CheckCommand.COMMAND:
        subcommand = command_dict.pop(ParserCommands.SUBCOMMAND)
    try:
        if command == ParserObjects.TASK:
            if subcommand == TaskCommands.AddSubcommand.COMMAND:
                try:
                    inteface.add_task(**command_dict)
                except EndTimeOverflowError as e:
                    print("! Oh! The subtask can't end later than its parent. Please check task id {}".format(e.args))
                except ValueError as e:
                    print("! Oh! The start time couldn't be less or than end time")

            elif subcommand == TaskCommands.EditSubcommand.COMMAND:
                task_id = command_dict[TaskCommands.EditSubcommand.ID]
                if command_dict[TaskCommands.EditSubcommand.EDIT_KIND] == TaskCommands.EditSubcommand.SET:
                    if command_dict[TaskAttributes.PRIORITY] is not None:
                        priority = command_dict[TaskAttributes.PRIORITY]
                        inteface.task_set_attribute(task_id, TaskAttributes.PRIORITY,priority)
                    elif command_dict[TaskAttributes.STATUS] is not None:
                        status = command_dict[TaskAttributes.STATUS]
                        inteface.task_set_attribute(task_id, TaskAttributes.STATUS,status)
                    elif command_dict[TaskAttributes.TITLE] is not None:
                        title = command_dict[TaskAttributes.TITLE]
                        inteface.task_set_attribute(task_id, TaskAttributes.TITLE,title)
                    elif command_dict[TaskAttributes.START_TIME] is not None:
                        try:
                            date = command_dict[TaskAttributes.START_TIME]
                            inteface.task_set_attribute(task_id, TaskAttributes.START_TIME, date)
                        except EndTimeOverflowError:
                            print("! Oh! The start time conflicts with task end time")
                    elif command_dict[TaskAttributes.END_TIME] is not None:
                        try:
                            date = command_dict[TaskAttributes.END_TIME]
                            inteface.task_set_attribute(task_id, TaskAttributes.END_TIME, date)
                        except EndTimeOverflowError:
                            print("! Oh! The end time conflicts with the start time or with parent task end time")
                elif command_dict[TaskCommands.EditSubcommand.EDIT_KIND] == TaskCommands.EditSubcommand.ADD:
                    if command_dict[TaskAttributes.TAGS] is not None:
                        tag = command_dict[TaskAttributes.TAGS]
                        inteface.task_add_attribute(task_id,TaskAttributes.TAGS,tag)
                    elif command_dict[TaskAttributes.CAN_EDIT] is not None:
                        user = command_dict[TaskAttributes.CAN_EDIT]
                        inteface.task_add_attribute(task_id,TaskAttributes.CAN_EDIT,user)
                    elif command_dict[TaskAttributes.REMIND_TIMES] is not None:
                        reminder = command_dict[TaskAttributes.REMIND_TIMES]
                        inteface.task_add_attribute(task_id, TaskAttributes.REMIND_TIMES, reminder)

                elif command_dict[TaskCommands.EditSubcommand.EDIT_KIND] == TaskCommands.EditSubcommand.RM:
                    if command_dict[TaskAttributes.TAGS] is not None:
                        tag = command_dict[TaskAttributes.TAGS]
                        inteface.task_remove_attribute(task_id,TaskAttributes.TAGS,tag)
                    elif command_dict[TaskAttributes.CAN_EDIT] is not None:
                        user = command_dict[TaskAttributes.CAN_EDIT]
                        inteface.task_remove_attribute(task_id,TaskAttributes.CAN_EDIT,user)
                    elif command_dict[TaskAttributes.REMIND_TIMES] is not None:
                        reminder = command_dict[TaskAttributes.REMIND_TIMES]
                        inteface.task_remove_attribute(task_id, TaskAttributes.REMIND_TIMES, reminder)


            elif subcommand == TaskCommands.RemoveSubcommand.COMMAND:
                try:
                    if command_dict[TaskCommands.RemoveSubcommand.F]:
                        for k in command_dict[TaskAttributes.UID]:
                            inteface.remove_with_subtasks(k)
                    else:
                        for k in command_dict[TaskAttributes.UID]:
                            inteface.remove_task(k)
                except SubtasksNotRemovedError:
                    print("! Oh! The task you're trying to delete has subtasks. Please remove them or use -f flag")

            elif subcommand == TaskCommands.FindSubcommand.COMMAND:
                tasks = list(inteface.find_tasks(**command_dict).values())
                for t in tasks:
                    printers.simple_task_printer(t)

            elif subcommand == TaskCommands.PrintSubcommand.COMMAND:
                if command_dict[TaskCommands.PrintSubcommand.ID]:
                    task = inteface.get_task(command_dict[TaskCommands.PrintSubcommand.ID])
                    printers.simple_task_printer(task, command_dict[TaskCommands.PrintSubcommand.WIDE])
                else:
                    tasks_d = inteface.tasks_manager.tasks
                    printers.hierarchy_printer(tasks_d,command_dict[TaskCommands.PrintSubcommand.WIDE])

            elif subcommand == TaskCommands.CompleteSubcommand.COMMAND:
                inteface.complete_task(command_dict[TaskAttributes.UID])
                print('Congratulations! :)')

        elif command == CheckCommand.COMMAND:
            date = dt.datetime.now()
            actual_tasks, reminders = inteface.check_time(date)
            priority = command_dict[CheckCommand.PRIORITY]
            status = command_dict[CheckCommand.STATUS]
            for each in reminders:
                if printers.task_satisfies(each, priority=priority, status=status):
                    printers.simple_reminder_printer(each)
            printers.simple_actual_tasks_printer(**actual_tasks, priority=priority,status=status)

        elif command == ParserObjects.PLAN:

            if subcommand == PlanCommands.AddSubcommand.COMMAND:
                period = parse_period(command_dict)
                end_time = command_dict[PlanCommands.AddSubcommand.FINISH]
                task_id = command_dict[PlanCommands.AddSubcommand.TASK_ID]
                task_template = inteface.get_task(task_id)
                try:
                    inteface.add_periodic_plan(period, task_template, task_id, end_time)
                except NoTimeValueError:
                    print("! Oh! Task '{}' has no start time specified. Can't set up a plan for it".format(task_id))
                inteface.check_plans()

            elif subcommand == PlanCommands.RemoveSubcommand.COMMAND:
                for k in command_dict[PlanCommands.RemoveSubcommand.PLAN_ID]:
                    inteface.rm_periodic_plan(k)

            elif subcommand == PlanCommands.PrintSubcommand.COMMAND:
                if command_dict[PlanCommands.PrintSubcommand.ID] is not None:
                    printers.simple_plan_printer(inteface.plans_manager.plans[command_dict[PlanCommands.PrintSubcommand.ID]])
                else:
                    for k, v in inteface.plans_manager.plans.items():
                        printers.simple_plan_printer(v)

        elif command == ParserObjects.USER:
            if subcommand == UserCommands.GET:
                print('USERNAME: {}'.format(inteface.current_user))
        return 0
    except PermissionError as e:
        print("! Oh! Permission denied for user: {}".format(inteface.current_user))
    except KeyError as e:
        print("! Oh! The key {} can't be found. Please check if it is correct".format(e.args))

if __name__ == '__main__':
    main()

