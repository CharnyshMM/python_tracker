"""Main classes described here:
    * Task
    * TaskList
    * DBManager
    """
import datetime
from collections import OrderedDict


class Task:
    """Base class for Task. Fields:
        * message
        * author
        * owner_link
        * creation_date
        * due_date
        * priority
        * tags[]
        * _subtasks - dict to store subtasks
    """
    def __init__(self, name, message, author, owner):
        self.name = name
        self.message = message
        self.author = author
        if owner is None:
            self.owner = self
        else:
            self.owner = owner
        self.creation_date = datetime.datetime.now()
        self.due_date = None
        self.priority = 5
        self.tags = list()
        self._subtasks = OrderedDict()

    def __str__(self):
        line = "\n TASK: " + self.name.upper()+"\n"
        line += "parent_task: "+self.owner.name+"\n"
        line += self.message.title() + "\n"
        line += "by: " + str(self.author)+"\n"
        line += "created: "+ str(self.creation_date)+"\n"
        line += "due: "+ str(self.due_date)+"\n"
        line += "priority: "+str(self.priority)+"\n"
        return line

    @staticmethod
    def wide_print(task,num=0):
        print(task)
        for i in task._subtasks:
            Task.wide_print(task._subtasks[i],num+1)

    def add_subtask(self, task, path):
        if len(path) > 1:
            self._subtasks.get(path[0]).add_subtask(task, path[1:])
        else:
            task.owner = self.owner
            self._subtasks[path[0]] = task

    def remove_subtask(self, path):
        if len(path) > 1:
            self._subtasks.get(path[0]).remove_task(path[1:])
        else:
            self._subtasks.pop(path[0])

    def get_subtask(self, path):
        task = self._subtasks.get(path[0])
        if len(path) > 1:
            return task.get_task(path[1:])
        else:
            return task

    def sort_subtasks_by_priority(self):
        self._subtasks = sorted(self._subtasks.items(),key=lambda k :(k[1].priority,k[0]))

    def sort_all_levels_by_priority(self):
        self.sort_subtasks_by_priority()
        for each in self._subtasks:
            self._subtasks[each].sort_all_levels_by_priority()

    def select_subtasks(self, key, result_dict=None):
        if result_dict is None:
            result_dict = OrderedDict()
        for (k,v) in self._subtasks.items():
            if key(v):
                result_dict[k] = v
            v.select_subtasks(key,result_dict)
        return result_dict


class Author:
    def __init__(self,name):
        self.name = name


class DashBoard(Task):
    def __init__(self,owner):
        super().__init__(owner)
        # add some fields




