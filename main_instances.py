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
    def __init__(self, message, author, owner):
        self.message = message
        self.author = author
        self.owner = owner
        self.creation_date = datetime.datetime.now()
        self.due_date = None
        self.priority = 5
        self.tags = list()
        self.subtasks = TaskList(self)
    def print_itself(self,tabs = 0):
        print(self.to_line(tabs))
        tabs += 1
        for each in self.subtasks:
            print(each.to_line(tabs))

    def to_line(self, tabs=0):
        tabs_before = "| "
        for i in range(tabs):
            tabs_before += " "
        line = tabs_before + self.message.title() + "\n"
        line += tabs_before + "by: " + str(self.author)+"\n"
        line += tabs_before + "created: "+ str(self.creation_date)+"\n"
        line += tabs_before + "due: "+ str(self.due_date)+"\n"
        line += tabs_before + "priority: "+str(self.priority)+"\n"
        line += "\\\n"
        return  line


class TaskList:
    """
    Base collection to store and unit multiple tasks
    """
    def __init__(self, owner):
        self.owner = owner
        self.__storage = list()
        self.actions_manager = None
        self.plans_manager = None

    def add_task(self, task):
        self.__storage.append(task)

    def find_task(self, task_template):
        pass

    def edit_task(self,task, edited_task):
        pass

    def serialize(self):
        pass;


class Author:
    def __init__(self,name):
        self.name = name

class DBManager:
    """Class that serializes & deserializes tasks """

    @classmethod
    def serialize_to_json(cls,task):
       pass

    def do_loarding(cls):
        return Task("THE DASHBOARD", Author("mikita"),None)
