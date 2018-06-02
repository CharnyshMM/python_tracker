from enum import Enum
from uuid import uuid1


class TaskAttributes(Enum):
    HAS_SUBTASKS = "has_subtasks"
    IS_SUBTASK_OF = "is_subtask_of"
    USER_TAGS = "user_tags"
    START_TIME = "start_time"
    REMIND_TIME = "remind_time"
    END_TIME = "end_time"
    AUTHOR = "author"
    #CAN_READ = "can_read"
    CAN_EDIT = "can_edit"
    NAME = "name"
    MESSAGE = "message"
    STATUS = "status"
    PRIORITY = "priority"
    UID = "uid"


class TaskStatus(Enum):
    ARCHIVED = "archived"
    ACTIVE = "active"
    COMPLITE = "complite"
    REJECTED = "rejected"


class TaskNode:
    def __init__(self, attributes_values):

        if TaskAttributes.NAME not in attributes_values:
            print("No name")
            raise BaseException()
        if TaskAttributes.AUTHOR not in attributes_values:
                 # raise AttributesMissingException
            raise BaseException()
        self.attributes = attributes_values
        self.attributes[TaskAttributes.CAN_EDIT] = [attributes_values[TaskAttributes.AUTHOR]]
        if TaskAttributes.UID not in attributes_values:
            self.attributes[TaskAttributes.UID] = uuid1()

    def __set_attribute(self,attr,val):
        # needs checking attr kind because of lists and single values
        self.attributes[attr] = val

    def __add_to_attribute(self,attr,val):
        # val should be a list
        # and i should check this

        if attr in self.attributes:
            self.attributes[attr].append(val)
        else:
            self.attributes[attr] = []

    def __unset_attribute(self,attr):
        # TODO:
        # need to forbid unsetting name or UID
        self.attributes.pop(attr)

    def __remove_from_attribute(self,attr,val):
        for i in self.attributes[attr]:
            if i == val:
                self.attributes[attr].remove(val)
                break
        # TODO: simplify
        if len(self.attributes[attr]) == 0:
            self.__unset_attribute(attr)

    def set_attribute(self,attr,val,user):
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__set_attribute(attr,val)

    def unset_attribute(self,attr,user):
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__unset_attribute(attr)

    def add_to_attribute(self,attr,val,user):
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__add_to_attribute(attr,val)

    def remove_from_attribute(self,attr,val, user):
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__remove_from_attribute(attr,val)

    def get_attribute(self,attr):
        return self.attributes[attr]

    def try_get_attribute(self,attr):
        if attr not in self.attributes:
            return None
        return self.attributes[attr]

    def has_attribute(self,attr):
        return attr in self.attributes



