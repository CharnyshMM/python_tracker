from json_db.json_storage import JsonStorage

class DB:
    def __init__(self):
        # TODO: loading from config
        self.json_storage = JsonStorage()

    def get_all_tasks(self):
        tasks_dict = self.json_storage.get_json_dict()
        return self.json_storage.task_collection_from_json(tasks_dict)

    def put_all_tasks(self, tasks_collection):
        tasks_dict = self.json_storage.task_collection_to_json(tasks_collection)
        self.json_storage.write_json_dict(tasks_dict)

    def get_all_users(self):
        pass

    def put_all_users(self,users_collection):
        pass
