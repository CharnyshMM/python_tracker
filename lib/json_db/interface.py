"""Simple Json DB interface"""

from lib.json_db.json_storage import JsonStorage
from lib.json_db.default_config import *
from lib.db_adapter import DBAdapter


class DB(DBAdapter):
    """This class wraps the JsonStorage class to provide required interface
    to be provided as a DB adapter for Interface class instance"""
    def __init__(self):
        if not os.path.isdir(DEFAULT_STORAGE_DIR):
            os.mkdir(DEFAULT_STORAGE_DIR)
        self.tasks_json_storage = JsonStorage(DEFAULT_TASKS_FILE)
        self.plans_json_storage = JsonStorage(DEFAULT_PLANS_FILE)

    def get_all_tasks(self):
        """Method gets all the tasks from file and returns a dict of them.
        return dict format {UUID uuid: Task task}
        """
        tasks_dict = self.tasks_json_storage.get_json_dict()
        return self.tasks_json_storage.task_collection_from_json(tasks_dict)

    def put_all_tasks(self, tasks_dict):
        """This method puts tasks dictionary tasks_collection to a file.
        The task_dict must have the format {UUID uuid: Task task}
        """
        tasks_dict = self.tasks_json_storage.task_collection_to_json(tasks_dict)
        self.tasks_json_storage.write_json_dict(tasks_dict)

    def put_all_plans(self,plans_dict):
        """This method takes plans_dict and puts it to a file
        The plans_dict must have the format {UUID uuid: Plan plan}
        """
        plans_dict = self.plans_json_storage.periodic_plans_dict_to_json(plans_dict)
        self.plans_json_storage.write_json_dict(plans_dict)

    def get_all_plans(self):
        """Method gets all the plans from file and returns a dict of them.
        return dict format {UUID uuid: Task task}
        """
        plans = self.plans_json_storage.get_json_dict()
        return self.plans_json_storage.periodic_plans_dict_from_json(plans)

