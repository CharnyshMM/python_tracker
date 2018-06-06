from json_db.json_storage import JsonStorage
from json_db.default_config import *

class DB:
    def __init__(self):
        # TODO: loading from config
        self.tasks_json_storage = JsonStorage(DEFAULT_TASKS_FILE)
        self.plans_json_storage = JsonStorage(DEFAULT_PLANS_FILE)

    def get_all_tasks(self):
        tasks_dict = self.tasks_json_storage.get_json_dict()
        return self.tasks_json_storage.task_collection_from_json(tasks_dict)

    def put_all_tasks(self, tasks_collection):
        tasks_dict = self.tasks_json_storage.task_collection_to_json(tasks_collection)
        self.tasks_json_storage.write_json_dict(tasks_dict)

    def get_all_users(self):
        pass

    def put_all_users(self,users_collection):
        pass

    def put_all_plans(self,plans_dict):
        plans_dict = self.plans_json_storage.periodic_plans_dict_to_json(plans_dict)
        self.plans_json_storage.write_json_dict(plans_dict)

    def get_all_plans(self):
        plans = self.plans_json_storage.get_json_dict()
        return self.plans_json_storage.periodic_plans_dict_from_json(plans)

