"""This module is a collection of simple printers for convinient console output"""

from lib.entities.task import TaskAttributes, TaskPriority
from collections import OrderedDict
import datetime as dt


def task_satisfies(task, priority=None, status=None):
    if priority is None and status is None:
        return True
    task_priority = task.get_attribute(TaskAttributes.PRIORITY)
    task_status = task.get_attribute(TaskAttributes.STATUS)
    satisfies = True
    if task_priority is not None and priority is not None and task_priority > priority:
        satisfies = False
    if task_status is not None and status is not None and task_status != status:
        satisfies = False
    return satisfies


def simple_task_printer(task, wide_print=False, indents=0):
    ind_str = ' | '*indents
    print(ind_str)
    print(ind_str + "---- TASK ----")
    print(ind_str + '= {}'.format(task.get_attribute(TaskAttributes.TITLE)))
    print(ind_str + 'UID: {}'.format(task.get_attribute(TaskAttributes.UID)))
    print(ind_str + 'Author: {}'.format(task.get_attribute(TaskAttributes.AUTHOR)))
    print(ind_str + 'Status: {}'.format(task.get_attribute(TaskAttributes.STATUS)))
    priority = task.get_attribute(TaskAttributes.PRIORITY)
    print(ind_str + 'Priority: {}'.format(TaskPriority.string_priority(priority)))
    print(ind_str + 'START DATE: {}'.format(task.try_get_attribute(TaskAttributes.START_TIME)))
    print(ind_str + 'END DATE: {}'.format(task.try_get_attribute(TaskAttributes.END_TIME)))
    print(ind_str + 'TAGS: {}'.format(task.try_get_attribute(TaskAttributes.TAGS)))
    if wide_print:
        reminders = task.try_get_attribute(TaskAttributes.REMIND_TIMES)
        if reminders is not None:
            print('REMINDERS SET:')
            for each in reminders:
                print(ind_str + " - {}".format(each))
        owner = task.try_get_attribute(TaskAttributes.PARENT)
        if owner is not None:
            print(ind_str + 'Is subtask of {}'.format(owner))
        subs = task.try_get_attribute(TaskAttributes.SUBTASKS)
        if subs is not None:
            print(ind_str + 'Has {} subtasks'.format(str(len(subs))))
        print(ind_str + 'USERS: {} can make changes here'.format(task.try_get_attribute(TaskAttributes.CAN_EDIT)))
        print(ind_str + 'PLAN ID: {} '.format(task.try_get_attribute(TaskAttributes.PLAN)))


def complex_task_printer(task, tasks_dict, wide_print=False):
    subtasks = gather_subtasks(task,tasks_dict)
    hierarchy_dict_printer(subtasks,tasks_dict,wide_print=wide_print)


def simple_reminder_printer(task):
    print("\n---- REMINDER ----")
    print('= {}'.format(task.get_attribute(TaskAttributes.TITLE)))
    print('START DATE: {}'.format(task.try_get_attribute(TaskAttributes.START_TIME)))
    print('END DATE: {}'.format(task.try_get_attribute(TaskAttributes.END_TIME)))
    print('TAGS {}'.format(task.try_get_attribute(TaskAttributes.TAGS)))


def simple_plan_printer(plan):
    print('\n---- PLAN ----')
    print('ID: {}'.format(plan.uid))
    print('for Task: {}'.format(plan.task_template.get_attribute(TaskAttributes.TITLE)))
    print('(Task ID: {})'.format(plan.task_id))
    print('Period: {}'.format(plan.period))
    print('Last appeared: {}'.format(plan.last_update_time))
    if plan.end_time is None:
        print('Ends: Never')
    else:
        print('Ends: {}'.format(plan.end_time))


def gather_subtasks(task, task_dict, hierarchy_dict=None):
    """
    creates an hierarchy_dict that represents the hierarchy of tasks in task dict
    :param task: top hierarchy task
    :param task_dict: all the tasks
    :param hierarchy_dict: recursively filled dict
    :return: hierarchy_dict
    """
    if hierarchy_dict is None:
        hierarchy_dict = OrderedDict()
    parent_id = task.get_attribute(TaskAttributes.UID)
    hierarchy_dict[parent_id] = OrderedDict()
    subtasks_ids = task.try_get_attribute(TaskAttributes.SUBTASKS)
    if subtasks_ids is None:
        return hierarchy_dict
    for i in subtasks_ids:
        if i in task_dict:
            gather_subtasks(task_dict[i],task_dict,hierarchy_dict[parent_id])
    return hierarchy_dict


def is_top_level_task(task, task_dict):
    parent_id = task.try_get_attribute(TaskAttributes.PARENT)
    if parent_id is None:
        return True
    elif parent_id not in task_dict:
        return True
    else:
        return False


def hierarchy_dict_printer(hierarchy_ids, task_dict, indents=0, wide_print=False, priority=None, status=None):
    """To print tasks in hierarchycal order if the hierarchy is already build"""
    for k,v in hierarchy_ids.items():
        if task_satisfies(task_dict[k], priority=priority, status=status):
            simple_task_printer(task_dict[k],indents=indents, wide_print=wide_print)
        hierarchy_dict_printer(v, task_dict, indents=indents + 1, wide_print=wide_print, priority=priority, status=status)


def hierarchy_printer(tasks_dict, date_sort_key=None, wide_print=False):
    """Builds a hierarchy for all the task in task_dict and prints them"""
    hier = OrderedDict()
    ordered_tasks_dict = OrderedDict(sorted(tasks_dict.items(), key=date_sort_key_builder(date_sort_key)))
    for k,v in ordered_tasks_dict.items():
        if is_top_level_task(v,ordered_tasks_dict):
            hier.update(gather_subtasks(v,ordered_tasks_dict))
    hierarchy_dict_printer(hier,ordered_tasks_dict, wide_print=wide_print)


def simple_actual_tasks_printer(starting, continuing, ending, priority=None, status=None):
    print('\n========== ACTUAL REPORT ==========')
    starting_hierarchy = OrderedDict()
    for k,v in starting.items():
        if is_top_level_task(v,starting):
            starting_hierarchy.update(gather_subtasks(v,starting))
    print("=== STARTING TASKS ===")
    hierarchy_dict_printer(starting_hierarchy, starting, priority=priority, status=status)

    continuing_hierarchy = OrderedDict()
    for k,v in continuing.items():
        if is_top_level_task(v,continuing):
            continuing_hierarchy.update(gather_subtasks(v,continuing))
    print("\n=== CONTINUING TASKS ===")
    hierarchy_dict_printer(continuing_hierarchy, continuing, priority=priority, status=status)

    ending_hierarchy = OrderedDict()
    for k,v in ending.items():
        if is_top_level_task(v,ending):
            ending_hierarchy.update(gather_subtasks(v,ending))
    print("\n=== ENDING TAKS ===")
    hierarchy_dict_printer(ending_hierarchy, ending, priority=priority, status=status)


def date_sort_key_builder(date_attribute=None):
    if date_attribute is None:
        date_attribute = TaskAttributes.START_TIME
    def key_func(k_v):
        date = k_v[1].try_get_attribute(date_attribute)
        if date is None:
            if date_attribute is TaskAttributes.START_TIME:
                return dt.datetime(1,1,1,0,0)
            elif date_attribute is TaskAttributes.END_TIME:
                return dt.datetime(9999,12,12,23,59)
        return date
    return key_func