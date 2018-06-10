r""" Task manager module contains a single TasksManager class"""

from lib.entities.task import *
import datetime as dt
from lib.logger import *
from lib.entities.exceptions import EndTimeOverflowError, SubtasksNotRemovedError



class TasksManager:
    r"""
    This class stores tasks in an inner dict and manages connections between them.
    Helps to safely add,remove, edit and search for a task
    """
    @log_decorator
    def __init__(self, tasks=None):
        if tasks is None:
            tasks = {}
        self.tasks = tasks

    @log_decorator
    def create_new_task(self, new_task, user):
        r"""
        Function to add a new task to others. Checks if the task doesn't conflict with existing ones and
        manages connections for parent and children if specified in the new task
        :param new_task: a new task to add
        :param user: a user who has permissions to edit the new task, its parent and children
        :return: None
        """
        if new_task.has_attribute(TaskAttributes.PARENT):
            parent_id = new_task.attributes[TaskAttributes.PARENT]
            this_id = new_task.attributes[TaskAttributes.UID]
            parent_task = self.tasks[parent_id]
            if not self.child_end_time_suits_parent(parent_task,new_task):
                raise EndTimeOverflowError(parent_id)
            self.tasks[parent_id].add_to_attribute(TaskAttributes.SUBTASKS,this_id,user)

        if new_task.has_attribute(TaskAttributes.SUBTASKS):
            this_id = new_task.attributes[TaskAttributes.UID]
            for sub_id in new_task.attributes[TaskAttributes.SUBTASKS]:
                sub_task = self.tasks[sub_id]
                if not self.child_end_time_suits_parent(new_task,sub_task):
                    raise EndTimeOverflowError(sub_id)
            for sub_id in new_task.attributes[TaskAttributes.SUBTASKS]:
                self.tasks[sub_id].set_attribute(TaskAttributes.PARENT, this_id, user)
        self.tasks[new_task.get_attribute(TaskAttributes.UID)] = new_task

    @log_decorator
    def remove_task(self, task_id,user):
        """
        Simply try to disconnect a task from a parent and remove a task
        :param task_id: id of task to be removed
        :param user: a user who has permissions to edit the new task, its parent and children
        :return: None
        """
        task = self.tasks[task_id]
        if task.has_attribute(TaskAttributes.SUBTASKS):
            raise SubtasksNotRemovedError(task_id)

        if task.has_attribute(TaskAttributes.PARENT):
            owner_id = task.get_attribute(TaskAttributes.PARENT)
            self.tasks[owner_id].remove_from_attribute(TaskAttributes.SUBTASKS, task_id, user)
        elif user not in task.get_attribute(TaskAttributes.CAN_EDIT):
            raise PermissionError("Deleting permitted for user '{}'".format(user))
        self.tasks.pop(task_id)

    @log_decorator
    def remove_with_subtasks(self,task_id,user):
        """
        Forse to delete a task with all its subtasks
        :param task_id: task id of task to be removed
        :param user: a user who has permissions to edit the new task, its parent and children
        :return: None
        """
        task = self.tasks[task_id]
        subtasks = task.try_get_attribute(TaskAttributes.SUBTASKS)
        if subtasks is not None:
            for sub_id in subtasks:
                self.remove_with_subtasks(sub_id,user)
        self.remove_task(task.get_attribute(TaskAttributes.UID),user)


    @log_decorator
    def find_task(self, attributes):
        """
        find a task(s) by attributes specified
        :param attributes: dict of TaskAttributes as keys and values
        :return: dict of suitable tasks
        """
        key_func = self.key_function_builder(attributes)
        return self.select_tasks_by_key(key_func)

    @log_decorator
    def get_task(self, task_id):
        return self.tasks[task_id]

    @log_decorator
    def get_all_tasks(self):
        return list(self.tasks.values())

    def edit_task_start_time(self,task_id,new_start_time, user):
        r"""
        Checks arguments and safely edits a start time for a task stored in the tasks_manager
        :param task_id: id of task to be edited
        :param new_start_time: new datetime.datetime time
        :param user: a user who has permissions to edit the new task, its parent and children
        :return: None
        """
        task = self.tasks[task_id]
        end_time = task.try_get_attribute(TaskAttributes.END_TIME)
        if end_time is None or new_start_time < end_time:
            task.set_attribute(TaskAttributes.START_TIME, new_start_time, user)
            return
        raise EndTimeOverflowError()

    def edit_task_end_time(self, task_id, new_end_time, user):
        r"""
        Checks arguments and safely edits a start time for a task stored in the tasks_manager
        :param task_id: id of task to be edited
        :param new_end_time: new datetime.datetime time
        :param user: a user who has permissions to edit the new task, its parent and children
        :return:
        """
        task = self.tasks[task_id]
        start_time = task.try_get_attribute(TaskAttributes.START_TIME)
        parent_id = task.try_get_attribute(TaskAttributes.PARENT)
        parent = self.tasks.get(parent_id,None)
        parent_end_time = None
        if parent is not None:
            parent_end_time = parent.try_get_attribute(TaskAttributes.END_TIME)

        parent_independent = (parent_id is None or parent_end_time is None or parent_end_time >= new_end_time)
        start_time_correct = start_time is None or start_time < new_end_time
        if parent_independent and start_time_correct:
            task.set_attribute(TaskAttributes.END_TIME, new_end_time, user)
            return
        raise EndTimeOverflowError()

    @log_decorator
    def select_actual_tasks(self, time, delta=None):
        r"""
        Select actual tasks from inner dict. Actualness is based on specified date(+/- delta).
        if delta is None delta = 5 minutes
        :param time: datetime.datetime
        :param delta: datetime.timedelta
        :return: dict {'starting': {}, 'continuing': {}, 'ending':{}}
        """
        if delta is None:
            delta = dt.timedelta(minutes=5)
        result_dict = {'starting': {}, 'continuing': {}, 'ending':{}}
        for k, v in self.tasks.items():
            start_time = v.try_get_attribute(TaskAttributes.START_TIME)
            if start_time is None:
                start_time = dt.datetime(1, 1, 1, 0, 0)
            end_time = v.try_get_attribute(TaskAttributes.END_TIME)
            if end_time is None:
                end_time = dt.datetime(9999, 12, 31, 23, 59, 59)
            if -delta <= start_time - time <= delta:
                result_dict['starting'][k] = v
            elif end_time - time <= delta:
                result_dict['ending'][k] = v
            elif start_time - time < -delta and end_time - time > delta:
                result_dict['continuing'][k] = v
        return result_dict

    @log_decorator
    def select_actual_reminders(self,date, delta=None):
        r"""
        Selects tasks with reminders actual on specified date(+/- delta).
        if delta is None delta = 5 minutes
        :param time: datetime.datetime
        :param delta: datetime.timedelta
        :return: dict of tasks that have actual reminders
        """
        if delta is None:
            delta = dt.timedelta(minutes=5)
        result_list = []
        for k, v in self.tasks.items():
            reminders = v.try_get_attribute(TaskAttributes.REMIND_TIMES)
            if reminders is None:
                continue
            for reminder in reminders:
                if -delta <= reminder - date <= delta:
                    result_list.append(v)
        return result_list

    def select_tasks_by_key(self, key):
        result_dict = dict()
        for k,v in self.tasks.items():
            if key(v):
                result_dict[k] = v

        return result_dict

    @staticmethod
    def key_function_builder(search_keys_dict):
        """
        Generates a key_function(task)
        It checks equalty of all attributes values specified in search_keys_dict to corresponding attribute values of
        task. And returns True if all are equal and False otherwice.
        :param search_keys_dict: attribute - value dict
        :return: key_fuction
        """
        def filter_function(task):
            for k, v in search_keys_dict.items():
                attr_val = task.try_get_attribute(k)
                if attr_val is None:
                    return False
                if isinstance(v, list):
                    for item in v:
                        if item not in attr_val:
                            return False
                elif attr_val != v:
                    return False
            return True

        return filter_function

    @staticmethod
    def child_end_time_suits_parent(parent, child):
        """
        Checks if parent's end time is greater that child's one
        :param parent: parent Task
        :param child: child Task
        :return: Boolean (True|False)
        """
        child_end_time = child.try_get_attribute(TaskAttributes.END_TIME)
        parent_end_time = parent.try_get_attribute(TaskAttributes.END_TIME)
        if parent_end_time is None:
            return True
        if child_end_time is None:
            return False
        if child_end_time <= parent_end_time:
            return True
        return False