import datetime
from uuid import uuid1
import copy


class TaskAttributes:
    SUBTASKS = "subtasks"  # mult []
    OWNED_BY = "owned_by"
    TAGS = "tags"          # mult []
    START_DATE = "start_date"
    REMIND_DATES = "remind_dates" # mult
    END_DATE = "end_date"
    AUTHOR = "author"
    CAN_EDIT = "can_edit"     # mult
    TITLE = "title"
    MESSAGE = "message"
    STATUS = "status"
    PRIORITY = "priority"
    UID = "uid"
    PLANS = "plans"           # mult


class TaskStatus:
    ARCHIVED = "archived"
    ACTIVE = "active"
    COMPLITE = "complete"
    REJECTED = "rejected"


class TaskPriority:
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class Task:
    def __init__(self, title, author, message=None, uid=None, start_date=None, remind_dates=None,
                 end_date=None, status=TaskStatus.ACTIVE, priority=TaskPriority.LOW, owned_by=None, subtasks=None, plans=None, can_edit=None, tags=None):
        self.attributes = {TaskAttributes.TITLE: title,
                           TaskAttributes.AUTHOR: author,
                           TaskAttributes.STATUS: status,
                           TaskAttributes.PRIORITY: priority,
                           }
        if start_date is not None:
            self.__set_attribute(TaskAttributes.START_DATE,start_date)
        if end_date is not None:
            self.__set_attribute(TaskAttributes.END_DATE,end_date)
        if remind_dates is not None:
            self.__set_attribute(TaskAttributes.REMIND_DATES,remind_dates)
        if owned_by is not None:
            self.__set_attribute(TaskAttributes.OWNED_BY,owned_by)
        if subtasks is not None:
            self.__set_attribute(TaskAttributes.SUBTASKS, subtasks)
        if plans is not None:
            self.__set_attribute(TaskAttributes.PLANS, plans)
        if tags is not None:
            self.__set_attribute(TaskAttributes.TAGS, tags)

        if can_edit is not None:
            self.attributes[TaskAttributes.CAN_EDIT] = can_edit
            if author not in can_edit:
                self.__add_to_list_attribute(TaskAttributes.CAN_EDIT,can_edit)
        else:
            self.__set_attribute(TaskAttributes.CAN_EDIT, [author])

        if uid is None:
            self.attributes[TaskAttributes.UID] = uuid1()
        else:
            self.attributes[TaskAttributes.UID] = uid

    def __set_attribute(self, attr, val):
        if attr not in [TaskAttributes.SUBTASKS,
                        TaskAttributes.REMIND_DATES,
                        TaskAttributes.PLANS,
                        TaskAttributes.TAGS,
                        TaskAttributes.CAN_EDIT
                        ]:
            self.attributes[attr] = val
        else:
            if isinstance(val, list):
                self.attributes[attr] = val
            else:
                self.attributes[attr] = [val]

    def __add_to_list_attribute(self, attr, val):
        if attr not in self.attributes:
            self.attributes[attr] = []
        if isinstance(val, list):
            self.attributes[attr] += val
        else:
            self.attributes[attr].append(val)

    def __unset_attribute(self, attr):
        # TODO:
        # need to forbid unsetting name or UID
        self.attributes.pop(attr)

    def __remove_from_list_attribute(self,attr,val):
        if not isinstance(val,list):
            val = [val]
        self.attributes[attr] = list(set(self.attributes[attr]) - set(val))
        if len(self.attributes[attr]) == 0:
            self.__unset_attribute(attr)

    def set_attribute(self,attr,val,user):
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__set_attribute(attr,val)

    def unset_attribute(self, attr, user):
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__unset_attribute(attr)

    def add_to_attribute(self, attr, val,user):
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__add_to_list_attribute(attr, val)

    def remove_from_attribute(self, attr, val, user):
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__remove_from_list_attribute(attr,val)

    def get_attribute(self, attr):
        return self.attributes[attr]

    def try_get_attribute(self, attr):
        if attr not in self.attributes:
            return None
        return self.attributes[attr]

    def has_attribute(self, attr):
        return attr in self.attributes

    def __str__(self):
        title = self.attributes[TaskAttributes.TITLE]
        uid = self.attributes[TaskAttributes.UID]
        return title + " " + str(uid)

    def __copy__(self):
        result_copy = {}
        for k,v in self.attributes.items():
            if isinstance(v,list):
                inner_copy = [copy.copy(x) for x in v]
                result_copy[k] = inner_copy
            else:
                result_copy[k] = copy.copy(v)
        return Task(**result_copy)
