from lib.task import TaskAttributes,TaskPlanAttributes,TaskStatus,TaskPriority


def simple_task_printer(task, indents=0):
    ind_str = ' | '*indents
    print(ind_str)
    print(ind_str + "---- TASK ----")
    print(ind_str + '= {}'.format(task.get_attribute(TaskAttributes.TITLE)))
    print(ind_str + 'UID: {}'.format(task.get_attribute(TaskAttributes.UID)))
    print(ind_str + 'Author: {}'.format(task.get_attribute(TaskAttributes.AUTHOR)))
    print(ind_str + 'TAGS {}'.format(task.try_get_attribute(TaskAttributes.TAGS)))
    owner = task.try_get_attribute(TaskAttributes.OWNED_BY)
    if owner is not None:
        print(ind_str + 'Is subtask of {}'.format(owner))
    subs = task.try_get_attribute(TaskAttributes.SUBTASKS)
    if subs is not None:
        print(ind_str + 'Has {} subtasks'.format(str(len(subs))))


def simple_reminder_printer(task):
    print("---- REMINDER ----")
    print('= {}'.format(task.get_attribute(TaskAttributes.TITLE)))
    print('TAGS {}'.format(task.try_get_attribute(TaskAttributes.TAGS)))


def gather_subtasks(task, task_dict, hierarchy_dict=None):
    if hierarchy_dict is None:
        hierarchy_dict = {}
    parent_id = task.get_attribute(TaskAttributes.UID)
    hierarchy_dict[parent_id] = {}
    subtasks_ids = task.try_get_attribute(TaskAttributes.SUBTASKS)
    if subtasks_ids is None:
        return hierarchy_dict
    for i in subtasks_ids:
        if i in task_dict:
            gather_subtasks(task_dict[i],task_dict,hierarchy_dict[parent_id])
    return hierarchy_dict


def is_top_level_task(task, task_dict):
    parent_id = task.try_get_attribute(TaskAttributes.OWNED_BY)
    if parent_id is None:
        return True
    elif parent_id not in task_dict:
        return True
    else:
        return False


def hierarchy_list_printer(hierarchy_ids, task_dict, indents=0):
    for k,v in hierarchy_ids.items():
        simple_task_printer(task_dict[k],indents)
        hierarchy_list_printer(v,task_dict,indents+1)



def simple_actual_tasks_printer(starting, continuing, ending):
    print('========== ACTUAL REPORT ==========')
    starting_hierarchy = {}
    for k,v in starting.items():
        if is_top_level_task(v,starting):
            starting_hierarchy.update(gather_subtasks(v,starting))
    print("=== STARTING TASKS ===")
    hierarchy_list_printer(starting_hierarchy,starting)

    continuing_hierarchy = {}
    for k,v in continuing.items():
        if is_top_level_task(v,continuing):
            continuing_hierarchy.update(gather_subtasks(v,continuing))
    print("\n=== CONTINUING TASKS ===")
    hierarchy_list_printer(continuing_hierarchy, continuing)

    ending_hierarchy = {}
    for k,v in ending.items():
        if is_top_level_task(v,ending):
            ending_hierarchy.update(gather_subtasks(v,ending))
    print("\n=== ENDING TAKS ===")
    hierarchy_list_printer(ending_hierarchy, ending)