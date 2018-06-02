from lib.task import *
from lib.tasks_collection import *
import datetime as dt
from lib.json_storage import JsonStorage

class TasksManager:
    def __init__(self,task_stor,user=None):
        self.tasks = task_stor
        self.current_user = user
        if task_stor is None:
            self.tasks = TasksCollection()

    def create_new_task(self, new_task):

        if new_task.has_attribute(TaskAttributes.IS_SUBTASK_OF) :
            owners_id = new_task.attributes[TaskAttributes.IS_SUBTASK_OF]
            this_id = new_task.attributes[TaskAttributes.UID]
            self.tasks.find_and_add_to_attribute(owners_id, TaskAttributes.HAS_SUBTASKS, this_id,self.current_user)

        if new_task.has_attribute(TaskAttributes.HAS_SUBTASKS):
            this_id = new_task.attributes[TaskAttributes.UID]
            for sub_id in new_task.attributes[TaskAttributes.HAS_SUBTASKS]:
                self.tasks.find_and_set_attribute(sub_id, TaskAttributes.IS_SUBTASK_OF,this_id,self.current_user)
        #after all the preparations and conntections performed
        self.tasks.add_task(new_task)

    def remove_task(self,task_id):
        # TODO:
        # try catch block needed
        task = self.tasks.find_task(task_id)
        if task.has_attribute(TaskAttributes.HAS_SUBTASKS):
            raise BaseException("task has subtasks, can't be removed")

        if task.has_attribute(TaskAttributes.IS_SUBTASK_OF):
            owner_id = task.get_arribute(TaskAttributes.IS_SUBTASK_OF)
            self.tasks.find_and_remove_from_attribute(owner_id, TaskAttributes.HAS_SUBTASKS, task_id, self.current_user)
        # TODO: check user permissions

        self.tasks.remove_task_by_id(id)

    def get_task(self, task_id):
        return self.tasks.find_task(task_id)

    def edit_task(self,task_id,edited_task):
        # TODO:
        # add try catch
        self.remove_task(task_id)
        edited_task.set_attribute(TaskAttributes.UID,task_id,self.current_user)
        self.create_new_task(edited_task)

    def set_task_status(self, task_id, status):
        if not isinstance(status,TaskStatus):
            raise TypeError()
        self.tasks.find_and_set_attribute(task_id, TaskAttributes.STATUS, status,self.current_user)


    def get_today_taskslist(self):
        return self.tasks.select_tasks_by_key(key=TasksManager.has_reminder_today)

    def initialise_from_DB(self):
        self.tasks = JsonStorage.task_collection_from_json(JsonStorage().getJsonDict())

    def save_to_DB(self):
        JsonStorage().writeJsonDict(JsonStorage.task_collection_to_json(self.tasks))
# TODO:
# - get the mathods below to a separate module
# - create a class FilterBuilder


    @staticmethod
    def has_reminder_today(task):
        val = task.try_get_attribute(TaskAttributes.REMIND_TIME)
        if val is None:
            return False
        if val.date() == dt.datetime.today().date():
            return True
        return False

    @staticmethod
    def has_subtasks(task):
        val = task.try_get_attribute(TaskAttributes.HAS_SUBTASKS)
        if val is not None and len(val)>0:
            return True
        return False

    @staticmethod
    def is_top_level_task(task):
        val = task.try_get_attribute(TaskAttributes.IS_SUBTASK_OF)
        if val is None:
            return True
        return False

