import json
import datetime as dt
from lib.tasks_collection import *
import uuid


class JsonStorage:
    def __init__(self):
        self.tasks_file = "../tasks.json"

    @staticmethod
    def task_to_json(task):
        j_dict = task.attributes
        j_dict[TaskAttributes.UID] = str(j_dict[TaskAttributes.UID])
        if TaskAttributes.REMIND_DATES in j_dict:
            dates = j_dict[TaskAttributes.REMIND_DATES]
            stamp_dates = [d.timestamp() for d in dates]
            j_dict[TaskAttributes.REMIND_DATES] = stamp_dates
        if TaskAttributes.START_DATE in j_dict:
            j_dict[TaskAttributes.START_DATE] = j_dict[TaskAttributes.START_DATE].timestamp()
        if TaskAttributes.END_DATE in j_dict:
            j_dict[TaskAttributes.END_DATE] = j_dict[TaskAttributes.END_DATE].timestamp()
        if TaskAttributes.SUBTASKS in j_dict:
            j_dict[TaskAttributes.SUBTASKS] = [str(i) for i in j_dict[TaskAttributes.SUBTASKS]]
        if TaskAttributes.OWNED_BY in j_dict:
            j_dict[TaskAttributes.OWNED_BY] = str(j_dict[TaskAttributes.OWNED_BY])
        return j_dict

    @staticmethod
    def task_from_json(j_dict):
        j_dict[TaskAttributes.UID] = uuid.UUID(j_dict[TaskAttributes.UID])
        if TaskAttributes.REMIND_DATES in j_dict:
            dates = j_dict[TaskAttributes.REMIND_DATES]
            j_dict[TaskAttributes.REMIND_DATES] = [dt.datetime.fromtimestamp(d) for d in dates]
        if TaskAttributes.END_DATE in j_dict:
            j_dict[TaskAttributes.END_DATE] = dt.datetime.fromtimestamp(j_dict[TaskAttributes.END_DATE])
        if TaskAttributes.START_DATE in j_dict:
            j_dict[TaskAttributes.START_DATE] = dt.datetime.fromtimestamp(j_dict[TaskAttributes.START_DATE])
        if TaskAttributes.SUBTASKS in j_dict:
            j_dict[TaskAttributes.SUBTASKS] = [uuid.UUID(i) for i in j_dict[TaskAttributes.SUBTASKS]]
        if TaskAttributes.OWNED_BY in j_dict:
            j_dict[TaskAttributes.OWNED_BY] = uuid.UUID(j_dict[TaskAttributes.OWNED_BY])
        return Task(**j_dict)

    @staticmethod
    def task_collection_to_json(collection):
        j_collection = dict()
        for k,v in collection.tasks.items():
            j_collection[str(k)] = JsonStorage.task_to_json(v)
        return j_collection

    @staticmethod
    def task_collection_from_json(j_dict):
        final_dict = {}
        for k,v in j_dict.items():
            final_dict[uuid.UUID(k)] = JsonStorage.task_from_json(v)
        return TasksCollection(final_dict)

    def read_string(self):
        contents = ""
        with open(self.tasks_file,"r") as file:
            contents = file.read()
        return contents

    def write_string(self, string):
        with open(self.tasks_file,"w") as file:
            file.write(string)

    def get_json_dict(self):
        try:
            contents = self.read_string()
        except FileNotFoundError:
            return {}
        return json.loads(contents)

    def write_json_dict(self, j_dict):
        self.write_string(json.JSONEncoder().encode(j_dict))