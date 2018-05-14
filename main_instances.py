"""Main classes described here:
    * Task
    * TaskList
    * DBManager
    """
import datetime as dt
from collections import OrderedDict
import copy


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


    def __init__(self, name, message, author, start_date=None, end_date=None, owner=None):
        self.name = name
        self.message = message
        self.author = author
        if owner is None:
            self.owner = self
        else:
            self.owner = owner
        self.__creation_date = dt.datetime.now()
        self.start_date = start_date
        self.end_date = end_date
        #self.due_date = None
        self.__priority = 3 # 1 <= priority <= 3
        self.tags = list()
        self._subtasks = OrderedDict()
        self.done = False


    def __str__(self):
        line = "\n TASK: " + self.name.upper()+"\n"
        line += "parent_task: "+self.owner.name+"\n"
        line += self.message.title() + "\n"
        line += "by: " + str(self.author)+"\n"
        line += "created: "+ str(self.creation_date)+"\n"
        line += "start_time: "+ str(self.start_date)+"\n"
        line += "end_time: " + str(self.end_date)+"\n"
        #line += "remind_set: "+ str(self.remind_date)+"\n"
        line += "priority: "+str(self.priority)+"\n"
        return line

    @property
    def creation_date(self):
        return self.__creation_date

    @creation_date.setter
    def creation_date(self,val):
        if val is None:
            self.__creation_date = dt.datetime.now()
        else:
            self.__creation_date = val

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self,val):
        if val is None:
            self.__start_date = dt.datetime.now()
        else:
            self.__start_date = val

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self,val):
        if val is None:
            self.__end_date = dt.datetime.max
        else:
            self.__end_date = val

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self,val):
        val = int(val)
        if val > 3:
            self.__priority = 3
        elif val < 1:
            self.__priority = 1
        else:
            self.__priority = val



    def add_subtask(self, task, path):
        if len(path) > 1:
            self._subtasks.get(path[0]).add_subtask(task, path[1:])
        else:
            task.owner = self
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

    def select_next_5_minutes_tasks(self, result_dict=None):
        if result_dict is None:
            result_dict = {"start": OrderedDict(), "continue": OrderedDict(), "end": OrderedDict()}
        for (k,v) in self._subtasks.items():
            if Task.starts_next_five_minutes(v):
                result_dict["start"][k] = v
            if Task.ends_next_five_minutes(v):
                result_dict["end"][k] = v
            if Task.continues_next_five_minutes(v):
                result_dict["continue"][k] = v
            v.select_next_5_minutes_tasks(result_dict)
        return result_dict

    # def select_multiple_keys(self,result_list_of_dicts = None, *keys):
    #     if len(keys) == 0 or keys is None:
    #         return None
    #     if result_list_of_dicts is None:
    #         result_list_of_dicts = [OrderedDict*len(keys)]
    #     for (k,v) in self._subtasks.items():
    #         for i in range(len(keys)):
    #             if keys[i](v):
    #                 result_list_of_dicts[i][k] = v
    #         v.select_multiple_keys(self, keys, result_list_of_dicts)
    #     return result_list_of_dicts

    def to_json_dict(self):
        d = {"name": self.name,
             "message": self.message,
             "author": str(self.author),
             "creation_date": str(self.creation_date),
             "start_date": str(self.start_date),
             "end_date": str(self.end_date),
             "priority": self.priority
             }
        sub_tasks = dict()
        for (k,v) in self._subtasks.items():
            sub_tasks[k] = v.to_json_dict()
        d["subtasks"] = sub_tasks
        return d

    @staticmethod
    def wide_print(task,num=0):
        print(task)
        for i in task._subtasks:
            Task.wide_print(task._subtasks[i],num+1)


    @staticmethod
    def from_dict(j_dict,owner):
        t = Task(j_dict["name"], j_dict["message"], Author(j_dict["author"]), None)
        t.creation_date = dt.datetime.strptime(j_dict["creation_date"], "%Y-%m-%d %H:%M:%S.%f")
        t.start_date = dt.datetime.strptime(j_dict["start_date"],"%Y-%m-%d %H:%M:%S.%f")
        t.end_date =dt.datetime.strptime(j_dict["end_date"],"%Y-%m-%d %H:%M:%S.%f")
        t.priority = j_dict["priority"]
        # tags +++
        if owner is None:
            t.owner = t
        else:
            owner.add_subtask(t, [t.name])
        for (k, v) in j_dict["subtasks"].items():
            t.add_subtask(Task.from_dict(v, t), [v["name"]])
        return t

    @staticmethod
    def is_today_task(task):
        if task.start_date.date() <= dt.date.today() and task.end_date.date() >= dt.date.today():
            return True
        return False

    @staticmethod
    def starts_next_five_minutes(task):
        delta = task.start_date - dt.datetime.now()
        if dt.timedelta() <= delta <= dt.timedelta(minutes=5):
            return True
        return False

    @staticmethod
    def ends_next_five_minutes(task):
        delta = task.end_date - dt.datetime.now()
        if dt.timedelta() <= delta <= dt.timedelta(minutes=5):
            return True
        return False

    @staticmethod
    def continues_next_five_minutes(task):
        if task.end_date - dt.datetime.now() > dt.timedelta(minutes=5):
            return True
        return False


class Author:
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return self.name


class Plan:
    def __init__(self, task_template, owner,  condition_checker=None,continue_if_rejected=False):
        self.task_template = task_template
        self.owner = owner
        self.continue_if_rejected = continue_if_rejected
        self.condition_checker = condition_checker
        self.condition = None


    def set_Next(self):
        if not self.condition_checker():
            return False

        task = copy.copy(self.task_template)
        #check this
        self.owner.add_subtask(task,[task.name])

    def set_periodic(self,start_time, timedelta):
        self.condition = {"type": "periodic", "timedelta":timedelta, "start": start_time}
        self.task_template.start_date = start_time + timedelta











