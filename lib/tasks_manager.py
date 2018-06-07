from lib.task import *
import datetime as dt
from lib.logger import *
from lib.decorators import key_function_builder
from lib.exceptions import *

class TasksManager:
    @log_decorator
    def __init__(self, tasks=None):
        if tasks is None:
            tasks = {}
        # self.current_user = user
        self.tasks = tasks

    # @log_decorator
    # def create_new_task(self, new_task):
    #     self.__create_new_task(new_task,self.current_user)

    @log_decorator
    def create_new_task(self,new_task, user):
        if new_task.has_attribute(TaskAttributes.OWNED_BY):
            owners_id = new_task.attributes[TaskAttributes.OWNED_BY]
            this_id = new_task.attributes[TaskAttributes.UID]
            self.tasks[owners_id].add_to_attribute(TaskAttributes.SUBTASKS,this_id,user)

        if new_task.has_attribute(TaskAttributes.SUBTASKS):
            this_id = new_task.attributes[TaskAttributes.UID]
            for sub_id in new_task.attributes[TaskAttributes.SUBTASKS]:
                self.tasks[sub_id].set_attribute(TaskAttributes.OWNED_BY,this_id,user)
        self.tasks[new_task.get_attribute(TaskAttributes.UID)] = new_task

    @log_decorator
    def remove_task(self, task_id,user):
        task = self.tasks[task_id]
        if task.has_attribute(TaskAttributes.SUBTASKS):
            raise SubtasksNotRemovedError(task_id)

        if task.has_attribute(TaskAttributes.OWNED_BY):
            owner_id = task.get_attribute(TaskAttributes.OWNED_BY)
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
        key_func = key_function_builder(attributes)
        return self.select_tasks_by_key(key_func)

    @log_decorator
    def get_task(self, task_id):
        return self.tasks[task_id]
        #return self.tasks.get_task(task_id)

    @log_decorator
    def get_all_tasks(self):
        return list(self.tasks.values())

    @log_decorator
    def edit_task(self,task_id,edited_task, user):
        # TODO:
        # add try catch
        self.remove_task(task_id,user)
        edited_task.set_attribute(TaskAttributes.UID,task_id, user)
        self.create_new_task(edited_task)

    @log_decorator
    def set_task_status(self, task_id, status, user):
        if not isinstance(status,TaskStatus):
            raise TypeError()
        self.tasks[task_id].set_attribute(TaskAttributes.STATUS, user)

    @log_decorator
    def select_actual_tasks(self, date, delta=None):
        if delta is None:
            delta = dt.timedelta(minutes=5)
        result_dict = {'starting': {}, 'continuing': {}, 'ending':{}}
        for k,v in self.tasks.items():
            start_date = v.try_get_attribute(TaskAttributes.START_DATE)
            if start_date is not None:
                start_delta = date - start_date
                if -delta <= start_delta < delta:
                    result_dict['starting'][k] = v
            end_date = v.try_get_attribute(TaskAttributes.END_DATE)
            if end_date is None:
                if k not in result_dict['starting']:
                    result_dict['continuing'][k] = v
            else:
                end_delta = end_date - date
                if end_delta >= dt.timedelta(0):
                    if end_delta <= delta:
                        result_dict['ending'][k] = v
                    else:
                        if v not in result_dict['starting']:
                            result_dict['continuing'][k] = v
        return result_dict

    @log_decorator
    def select_actual_reminders(self,date,delta=None):
        if delta is None:
            delta = dt.timedelta(minutes=5)
        result_list = []
        for k, v in self.tasks.items():
            reminders = v.try_get_attribute(TaskAttributes.REMIND_DATES)
            if reminders is None:
                continue
            for reminder in reminders:
                if dt.timedelta(0) <= reminder - date <= delta:
                    result_list.append(v)
        return result_list

    def select_tasks_by_key(self, key):
        result_dict = dict()
        for k,v in self.tasks.items():
            if key(v):
                result_dict[k] = v

        return result_dict
