import main_instances as mi
#import console_interactions as console
#import datetime


    #организовать определение и построение пути к задаче

class SessionManager:
    def __init__(self, user):
        t =  mi.Author("mikita")
        self.main_task = mi.Task("MainTask","Main task mess",t,t)

    def print_dashboard(self):
        for each in self.main_task.subtasks:
            each.to_line(0);

    def add_task(self, task, path):
        self.main_task.subtasks.add_task(task, path)

    def remove_task(self, path):
        self.main_task.subtasks.remove_task(path)
