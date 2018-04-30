"""Main istances decribed here:
    * Task
    * TaskList
    * DBManager
    """
import datetime


class Task:
    """Base class for Task. Fields:
        * message
        * author
        * owner_link
        * creation_date
        * due_date
        * priority
        * tags[]
        * subtasks
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
        self.subtasks = TaskList(self)

    def __str__(self):
        line = "\n TASK: " + self.name.upper()+"\n"
        line += "parent_task: "+self.owner.name+"\n"
        line += self.message.title() + "\n"
        line += "by: " + str(self.author)+"\n"
        line += "created: "+ str(self.creation_date)+"\n"
        line += "due: "+ str(self.due_date)+"\n"
        line += "priority: "+str(self.priority)+"\n"
        return line

    def str_generator (self):
        for each in self.subtasks:
            yield each.str_generator()
        yield self.__str__()

    def poisk_w_shirinu(self):
        yield TaskList.poisk_w_shirinu(self)


    @staticmethod
    def wide_print(task,num=0):
        print(task)
        for i in task.subtasks._storage:
            Task.wide_print(task.subtasks._storage[i],num+1)


class TaskList:
    """
    Base collection to store and unit multiple tasks
    """
    def __init__(self, owner):
        self.owner = owner
        self._storage = dict()
        self.actions_manager = None
        self.plans_manager = None

    def add_task(self, task, path):
        if len(path) > 1:
            self._storage.get(path[0]).subtasks.add_task(task, path[1:])
        else:
            task.owner = self.owner
            self._storage[path[0]] = task
        # path[last_item] is new task.name


    def remove_task(self, path):
        if len(path) > 1:
            self._storage.get(path[0]).subtasks.remove_task(path[1:])
        else:
            self._storage.pop(path[0])

    def get_task(self, path):
        task = self._storage.get(path[0])
        if len(path) > 1:
            return task.subtasks.get_task(path[1:])
        else:
            return task
    # по идее, адд может работать как эдит

    def iterate(self):
        for each in self._storage:
             yield self._storage[each]

    @staticmethod
    def poisk_w_shirinu(item):
        yield item
        for each in item._storage:
            TaskList.poisk_w_shirinu(each)


class Author:
    def __init__(self,name):
        self.name = name


class DashBoard(TaskList):
    def __init__(self,owner):
        super().__init__(owner)
        # add some fields




