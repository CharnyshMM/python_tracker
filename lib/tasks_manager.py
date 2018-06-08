from lib.task import *
import datetime as dt
from lib.logger import *

from lib.exceptions import EndTimeOverflowError, SubtasksNotRemovedError


class TasksManager:
    @log_decorator
    def __init__(self, tasks=None):
        if tasks is None:
            tasks = {}
        self.tasks = tasks

    @log_decorator
    def create_new_task(self, new_task, user):
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
        task = self.tasks[task_id]
        subtasks = task.try_get_attribute(TaskAttributes.SUBTASKS)
        if subtasks is not None:
            for sub_id in subtasks:
                self.remove_with_subtasks(sub_id,user)
        self.remove_task(task.get_attribute(TaskAttributes.UID),user)


    @log_decorator
    def find_task(self, attributes):
        key_func = self.key_function_builder(attributes)
        return self.select_tasks_by_key(key_func)

    @log_decorator
    def get_task(self, task_id):
        return self.tasks[task_id]

    @log_decorator
    def get_all_tasks(self):
        return list(self.tasks.values())

    def edit_task_start_time(self,task_id,new_start_time, user):
        task = self.tasks[task_id]
        end_time = task.try_get_attribute(TaskAttributes.END_TIME)
        if end_time is None or new_start_time < end_time:
            task.set_attribute(TaskAttributes.START_TIME, new_start_time, user)
            return
        raise EndTimeOverflowError()

    def edit_task_end_time(self, task_id, new_end_time, user):
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
        if delta is None:
            delta = dt.timedelta(minutes=5)
        result_dict = {'starting': {}, 'continuing': {}, 'ending':{}}
        for k, v in self.tasks.items():
            start_time = v.try_get_attribute(TaskAttributes.START_TIME)
            if start_time is None:
                start_time = dt.datetime(1,1,1,0,0)
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
        child_end_time = child.try_get_attribute(TaskAttributes.END_TIME)
        parent_end_time = parent.try_get_attribute(TaskAttributes.END_TIME)
        if parent_end_time is None:
            return True
        if child_end_time is None:
            return False
        if child_end_time <= parent_end_time:
            return True
        return False