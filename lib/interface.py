from tasks_manager import *
from decorators import *


class Interface:
    tasks_manager = None

    @classmethod
    def initialise(cls,user):
        cls.tasks_manager = TasksManager(None, user=user)
        cls.tasks_manager.initialise_from_DB()

    @classmethod
    def add_task(cls, name, author, start_date=None,
                 end_date=None, remind_dates=None, owning_task=None, subtasks=None):
        params_dict = {TaskAttributes.NAME: name,TaskAttributes.AUTHOR: author}
        if start_date is not None:
            params_dict[TaskAttributes.START_TIME] = start_date
        if end_date is not None:
            params_dict[TaskAttributes.END_TIME] = end_date
        if remind_dates is not None:
            params_dict[TaskAttributes.REMIND_TIME] = remind_dates
        if owning_task is not None:
            params_dict[TaskAttributes.IS_SUBTASK_OF] = owning_task
        if subtasks is not None:
            params_dict[TaskAttributes.HAS_SUBTASKS] = subtasks
        cls.tasks_manager.create_new_task(TaskNode(params_dict))

    @classmethod
    def remove_task(cls, task_id):
        cls.tasks_manager.remove_task(task_id)

    @classmethod
    def get_task(cls, task_id):
        return cls.tasks_manager.get_task(task_id)

    @classmethod
    def edit_task(cls, task_id, name=None, author=None, start_date=None,
                  end_date=None, remind_dates=None, owning_task=None, subtasks=None, tags=None):
        params_dict = {}
        if name is not None:
            params_dict[TaskAttributes.NAME] = name
        if author is not None:
            params_dict[TaskAttributes.AUTHOR] = author
        if start_date is not None:
            params_dict[TaskAttributes.START_TIME] = start_date
        if end_date is not None:
            params_dict[TaskAttributes.END_TIME] = end_date
        if remind_dates is not None:
            params_dict[TaskAttributes.REMIND_TIME] = remind_dates
        if owning_task is not None:
            params_dict[TaskAttributes.IS_SUBTASK_OF] = owning_task
        if subtasks is not None:
            params_dict[TaskAttributes.HAS_SUBTASKS] = subtasks
        if tags is not None:
            params_dict[TaskAttributes.USER_TAGS] = tags

        cls.tasks_manager.edit_task(task_id, params_dict)

    @classmethod
    def find_tasks(cls, name=None, author=None, start_date=None,
                  end_date=None, remind_dates=None, owning_task=None, subtasks=None, tags=None):
        params_dict = {}
        if name is not None:
            params_dict[TaskAttributes.NAME] = name
        if author is not None:
            params_dict[TaskAttributes.AUTHOR] = author
        if start_date is not None:
            params_dict[TaskAttributes.START_TIME] = start_date
        if end_date is not None:
            params_dict[TaskAttributes.END_TIME] = end_date
        if remind_dates is not None:
            params_dict[TaskAttributes.REMIND_TIME] = remind_dates
        if owning_task is not None:
            params_dict[TaskAttributes.IS_SUBTASK_OF] = owning_task
        if subtasks is not None:
            params_dict[TaskAttributes.HAS_SUBTASKS] = subtasks
        if tags is not None:
            params_dict[TaskAttributes.USER_TAGS] = tags

        return cls.tasks_manager.tasks.select_tasks_by_key(build_filter_function(params_dict))

    @classmethod
    def get_all_tasks(cls):
        return cls.tasks_manager.tasks.get_all_tasks()

    @classmethod
    def check_time(cls):
        pass

