from main_instances import *
from time_manager import TimeManager
from decorators import Filters
#import console_interactions as console
#import datetime

    #организовать определение и построение пути к задаче

class Session:
    def __init__(self, username):
        t =  Author(username)
        self.main_task = Task("MainTask","Main task mess",t)
        self.time_manager = TimeManager(self.main_task)

    def add_task(self, task, path):
        self.main_task.add_subtask(task, path)

    def remove_task(self, path):
        self.main_task.remove_subtask(path)

    def check(self):
        return self.time_manager.get_next_five_minutes()

    def get_task(self,path=None):
        if path is None:
            path = []  # return all tasks
        return self.main_task.get_subtask(path)

    def select_task(self,selector):
        return self.main_task.select_subtasks(key=selector)

    def select_by_tag(self, tags):
        return self.main_task.select_tasks_by_tags(tags)






