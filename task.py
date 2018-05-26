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
    CAN_READ = "can_read"
    CAN_EDIT = "can_edit"
    NAME = "name"
    MESSAGE = "message"
    STATUS = "status"
    PRIORITY = "priority"
    UID = "uid"


    @classmethod
    def attributes_equalty(cls, attr, val1, val2):
        is_list_attr = (attr == cls.USER_TAGS or attr == cls.REMIND_TIME or
                        attr == cls.CAN_EDIT or attr == cls.CAN_READ or attr == cls.HAS_SUBTASKS)
        if is_list_attr:
            if len(val1) != len(val2):
                return False
            for v1 in val1:
                if v1 not in val2:
                    return False
        else:
            if val1 != val2:
                return False
        return True

    @classmethod
    def includes_attributes(cls, attr, val_to_find, val_to_check):
        #check length and raise Error if Zero
        is_list_attr = (attr == cls.USER_TAGS or attr == cls.REMIND_TIME or
                        attr == cls.CAN_EDIT or attr == cls.CAN_READ or attr == cls.HAS_SUBTASKS)
        if is_list_attr:
            for v1 in val_to_find:
                if v1 not in val_to_check:
                    return False
        else:
            if val_to_find != val_to_check:
                return False
        return True


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
            print("No author")
            raise BaseException()
        self.attributes = attributes_values
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
        # check the user permissions
        self.__set_attribute(attr,val)

    def unset_attribute(self,attr,user):
        self.__unset_attribute(attr)

    def add_to_attribute(self,attr,val,user):
        self.__add_to_attribute(attr,val)

    def remove_from_attribute(self,attr,val, user):
        self.__remove_from_attribute(attr,val)

    def get_attribute(self,attr):
        return self.attributes[attr]

    def try_get_attribute(self,attr):
        if attr not in self.attributes:
            return None
        return self.attributes[attr]

    def has_attribute(self,attr):
        return attr in self.attributes



