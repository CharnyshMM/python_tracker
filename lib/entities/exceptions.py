r""" Module contains exception types used in Py_Tracker lib package.

"""


class AttributeMissingError (AttributeError):
    """Derived from AttributeError. This is raised when required task attribute is missing"""
    pass

class SubtasksNotRemovedError(AttributeError):
    """Derived from AttributeError. This is raised when trying to simply remove a task that has subtasks"""
    pass

class EndTimeOverflowError(ValueError):
    """Derived from ValueError. THis is raised in case of conflicting end times for parent-child tasks"""
    pass

class NoTimeValueError(ValueError):
    """Derived from ValueError. This is raised if the task doesn't have some time set when it is required"""
    pass


