import json
import datetime as dt
from lib.tasks_collection import *
import uuid

class JsonStorage:
    def __init__(self):
        self.tasks_file = "tasks.json"

    @staticmethod
    def task_to_json(task):
        j_dict = task.attributes
        j_dict[TaskAttributes.UID] = str(j_dict[TaskAttributes.UID])
        if TaskAttributes.REMIND_TIME in j_dict:
            dates = j_dict[TaskAttributes.REMIND_TIME]
            stamp_dates = [d.timestamp() for d in dates]
            j_dict[TaskAttributes.REMIND_TIME] = stamp_dates
        if TaskAttributes.START_TIME in j_dict:
            j_dict[TaskAttributes.START_TIME] = j_dict[TaskAttributes.START_TIME].timestamp()

        if TaskAttributes.END_TIME in j_dict:
            j_dict[TaskAttributes.END_TIME] = j_dict[TaskAttributes.END_TIME].timestamp()

        if TaskAttributes.HAS_SUBTASKS in j_dict:
            j_dict[TaskAttributes.HAS_SUBTASKS] = [str(i)for i in j_dict[TaskAttributes.HAS_SUBTASKS]]
        if TaskAttributes.IS_SUBTASK_OF in j_dict:
            j_dict[TaskAttributes.IS_SUBTASK_OF] = str(j_dict[TaskAttributes.IS_SUBTASK_OF])


        # TODO:
        # same translation for plans
        final_dict = {}
        for k,v in j_dict.items():

            final_dict[k.value] = v

        return final_dict


    @staticmethod
    def task_from_json(j_dict):
        final_dict = {}
        for k,v in j_dict.items():
            final_dict[TaskAttributes(k)] = v

        j_dict = final_dict

        j_dict[TaskAttributes.UID] = uuid.UUID(j_dict[TaskAttributes.UID])
        if TaskAttributes.REMIND_TIME in j_dict:
            dates = j_dict[TaskAttributes.REMIND_TIME]
            j_dict[TaskAttributes.REMIND_TIME] = [dt.datetime.fromtimestamp(d) for d in dates]
        if TaskAttributes.END_TIME in j_dict:
            j_dict[TaskAttributes.END_TIME] = dt.datetime.fromtimestamp(j_dict[TaskAttributes.END_TIME])

        if TaskAttributes.START_TIME in j_dict:
            j_dict[TaskAttributes.START_TIME] = dt.datetime.fromtimestamp(j_dict[TaskAttributes.START_TIME])

        if TaskAttributes.HAS_SUBTASKS in j_dict:
            j_dict[TaskAttributes.HAS_SUBTASKS] = [uuid.UUID(i) for i in j_dict[TaskAttributes.HAS_SUBTASKS]]
        if TaskAttributes.IS_SUBTASK_OF in j_dict:
            j_dict[TaskAttributes.IS_SUBTASK_OF] = uuid.UUID(j_dict[TaskAttributes.IS_SUBTASK_OF])

        return Task(j_dict)

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

    def readString(self):
        contents = ""
        with open(self.tasks_file,"r") as file:
            contents = file.read()
        return contents

    def writeString(self, string):
        with open(self.tasks_file,"w") as file:
            file.write(string)

    def getJsonDict(self):
        contents = self.readString()
        return json.loads(contents)

    def writeJsonDict(self, j_dict):
        self.writeString(json.JSONEncoder().encode(j_dict))