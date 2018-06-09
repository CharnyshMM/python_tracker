""" Task module includes classes that are used to describe a Task"""


from uuid import uuid1
import copy



class TaskAttributes:
    r"""
        Class that just stores single Task attributes
        TITLE - a title of task(Can't be None)
        SUBTASKS - child tasks connected to a task. They can't end later than their parent
        PARENT - id of parent task
        TAGS - user defined key_words
        STARTTIME - when the task starts
        END_TIME - when the task ends
        REMINS_TIMES - list of times when to remind about the task
        AUTHOR - a username of him who created a task(Can't be None)
        CAN_EDIT - list of usernames who can make changes in task
        STATUS - one of fixed TaskStatus sttuses
        PRIORITY - one of fixed in TaskPriority priorities
        UID - unique id of a task
        PLAN - id of PeriodicPlan object if this task was created automatically by it
    """
    SUBTASKS = "subtasks"
    PARENT = "parent"
    TAGS = "tags"
    START_TIME = "start_time"
    REMIND_TIMES = "remind_times"
    END_TIME = "end_time"
    AUTHOR = "author"
    CAN_EDIT = "can_edit"
    TITLE = "title"
    STATUS = "status"
    PRIORITY = "priority"
    UID = "uid"
    PLAN = "plan"


class TaskStatus:
    """Just task status"""
    ACTIVE = "active"
    COMPLETE = "complete"



class TaskPriority:
    """Task Priority"""
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    @classmethod
    def string_priority(cls, priority):
        """converts int priority to string"""
        if priority == cls.HIGH:
            return 'HIGH'
        if priority == cls.MEDIUM:
            return 'MEDIUM'
        if priority == cls.LOW:
            return 'LOW'

class Task:
    def __init__(self, title, author, uid=None, start_time=None, remind_times=None,
                 end_time=None, status=TaskStatus.ACTIVE, priority=TaskPriority.MEDIUM, parent=None, subtasks=None, plan=None, can_edit=None, tags=None):
        self.attributes = {TaskAttributes.TITLE: title,
                           TaskAttributes.AUTHOR: author,
                           TaskAttributes.STATUS: status,
                           TaskAttributes.PRIORITY: priority,
                           }
        if start_time is not None and end_time is not None:
            if start_time >= end_time:
                raise ValueError("start_time is greater than end_time")
        if start_time is not None:
            self.__set_attribute(TaskAttributes.START_TIME, start_time)
        if end_time is not None:
            self.__set_attribute(TaskAttributes.END_TIME, end_time)
        if remind_times is not None:
            self.__set_attribute(TaskAttributes.REMIND_TIMES, remind_times)
        if parent is not None:
            self.__set_attribute(TaskAttributes.PARENT, parent)
        if subtasks is not None:
            self.__set_attribute(TaskAttributes.SUBTASKS, subtasks)
        if plan is not None:
            self.__set_attribute(TaskAttributes.PLAN, plan)
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

        """
        Set attribute means to set the whole value.
        private function to set attribute without checking user

        :param attr: TaskAttribute attribute
        :param val: Value, a list or a single one
        """
        if val is None:
            return
        if attr not in [TaskAttributes.SUBTASKS,
                        TaskAttributes.REMIND_TIMES,
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
        """
        Private add_to_Attribute, doen't check user permissions
         :param attr: TaskAttribute attribute
        :param val: Value, a list or a single one
        :return: None
        """
        if attr not in self.attributes:
            self.attributes[attr] = []
        if isinstance(val, list):
            self.attributes[attr] += val
        else:
            self.attributes[attr].append(val)

    def __unset_attribute(self, attr):
        """
        Private unset. Just removes the attribute
        :param attr: TaskAttribute to be removed
        :return:
        """
        self.attributes.pop(attr)

    def __remove_from_list_attribute(self,attr,val):
        """
        Private. To pop some values of list attributes
         :param attr: TaskAttribute attribute
        :param val: Value, a list or a single one
        :return: None
        """
        if not isinstance(val,list):
            val = [val]
        self.attributes[attr] = list(set(self.attributes[attr]) - set(val))
        if len(self.attributes[attr]) == 0:
            self.__unset_attribute(attr)

    def set_attribute(self,attr,val,user):
        """
        Sets the attribute value. Checks user permissions. Can raise a permission error.
        :param attr: TaskAttribute attribute
        :param val: Value, a list or a single one
        :param user: username
        :return: None

        """
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__set_attribute(attr,val)

    def unset_attribute(self, attr, user):
        """
        Completely removes attribute.Checks user permissions.Can raise a permission error.
        :param attr: TaskAttribute attribute
        :param user: username
        :return: None
        """
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__unset_attribute(attr)

    def add_to_attribute(self, attr, val,user):
        """
        Adds a value to a list attribute. Checks user permissions. Can raise a permission error.
        :param attr: TaskAttribute attribute
        :param val: value to add. A list or a single one
        :param user: username
        :return:
        """
        if user not in self.attributes[TaskAttributes.CAN_EDIT]:
            raise PermissionError()
        self.__add_to_list_attribute(attr, val)

    def remove_from_attribute(self, attr, val, user):
        """
        Pop some values from attribute. (Checks user permissions). Can raise a permission error.
        :param attr: TaskAttribute attribute
        :param val: Value, a list or a single one
        :param user: username
        :return: None
        """
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
