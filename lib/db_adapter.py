"""This file contains empty DB interface class"""

class DBAdapter:
    """
    This class is used to connect custom DB to Py_Tracker library Interface class.

    Class just defines methods that must be overloaded by a DB interface that is passed
    as a parameter to Interface class init. These methods are used inside Interface instance
     to communicate with DB.
    """

    def get_all_tasks(self):
        """
        This method must return a dict of tasks from a DB.

        :return = {UUID(some_task_uuid) : Task(some_task)}"""
        pass

    def put_all_tasks(self, tasks_collection):
        """
        This method takes a tasks dict and writes it into a DB.

        tasks_collection = {UUID(some_task_uuid) : Task(some_task)}
        """
        pass

    def get_all_plans(self):
        pass

    def put_all_plans(self, plans_dict):
        pass