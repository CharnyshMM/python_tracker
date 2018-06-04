from lib.task import TaskAttributes,TaskPlanAttributes,TaskStatus,TaskPriority


def simple_task_printer(task):
    print("---- TASK ----")
    print(task.get_attribute(TaskAttributes.TITLE))
    print('UID: {}'.format(task.get_attribute(TaskAttributes.UID)))
    print('Author: {}'.format(task.get_attribute(TaskAttributes.AUTHOR)))
    print('TAGS {}'.format(task.try_get_attribute(TaskAttributes.TAGS)))
    owner = task.try_get_attribute(TaskAttributes.OWNED_BY)
    if owner is not None:
        print('Is subtask of {}'.format(owner))
    subs = task.try_get_attribute(TaskAttributes.SUBTASKS)
    if subs is not None:
        print('Has {} subtasks'.format(str(len(subs))))

