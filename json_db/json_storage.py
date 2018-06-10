import json
import uuid
from lib.entities.task import *
from lib.entities.plan import *


class JsonStorage:
    def __init__(self, file):
        self.file = file

    @staticmethod
    def task_to_json(task):
        j_dict = copy.deepcopy(task.attributes)
        j_dict[TaskAttributes.UID] = str(j_dict[TaskAttributes.UID])
        if TaskAttributes.REMIND_TIMES in j_dict:
            dates = j_dict[TaskAttributes.REMIND_TIMES]
            stamp_dates = [d.timestamp() for d in dates]
            j_dict[TaskAttributes.REMIND_TIMES] = stamp_dates
        if TaskAttributes.START_TIME in j_dict:
            j_dict[TaskAttributes.START_TIME] = j_dict[TaskAttributes.START_TIME].timestamp()
        if TaskAttributes.END_TIME in j_dict:
            j_dict[TaskAttributes.END_TIME] = j_dict[TaskAttributes.END_TIME].timestamp()
        if TaskAttributes.SUBTASKS in j_dict:
            j_dict[TaskAttributes.SUBTASKS] = [str(i) for i in j_dict[TaskAttributes.SUBTASKS]]
        if TaskAttributes.PARENT in j_dict:
            j_dict[TaskAttributes.PARENT] = str(j_dict[TaskAttributes.PARENT])
        if TaskAttributes.PLAN in j_dict:
            j_dict[TaskAttributes.PLAN] = str(j_dict[TaskAttributes.PLAN])
        return j_dict

    @staticmethod
    def task_from_json(j_dict):
        j_dict[TaskAttributes.UID] = uuid.UUID(j_dict[TaskAttributes.UID])
        if TaskAttributes.REMIND_TIMES in j_dict:
            dates = j_dict[TaskAttributes.REMIND_TIMES]
            j_dict[TaskAttributes.REMIND_TIMES] = [dt.datetime.fromtimestamp(d) for d in dates]
        if TaskAttributes.END_TIME in j_dict:
            j_dict[TaskAttributes.END_TIME] = dt.datetime.fromtimestamp(j_dict[TaskAttributes.END_TIME])
        if TaskAttributes.START_TIME in j_dict:
            j_dict[TaskAttributes.START_TIME] = dt.datetime.fromtimestamp(j_dict[TaskAttributes.START_TIME])
        if TaskAttributes.SUBTASKS in j_dict:
            j_dict[TaskAttributes.SUBTASKS] = [uuid.UUID(i) for i in j_dict[TaskAttributes.SUBTASKS]]
        if TaskAttributes.PARENT in j_dict:
            j_dict[TaskAttributes.PARENT] = uuid.UUID(j_dict[TaskAttributes.PARENT])
        if TaskAttributes.PLAN in j_dict:
            j_dict[TaskAttributes.PLAN] = uuid.UUID(j_dict[TaskAttributes.PLAN])
        return Task(**j_dict)

    @staticmethod
    def task_collection_to_json(tasks_dict):
        j_collection = dict()
        for k,v in tasks_dict.items():
            j_collection[str(k)] = JsonStorage.task_to_json(v)
        return j_collection

    @staticmethod
    def task_collection_from_json(j_dict):
        final_dict = {}
        for k,v in j_dict.items():
            final_dict[uuid.UUID(k)] = JsonStorage.task_from_json(v)
        return final_dict

    def read_string(self):
        contents = ""
        with open(self.file, "r") as file:
            contents = file.read()
        return contents

    def write_string(self, string):
        with open(self.file, "w") as file:
            file.write(string)

    def get_json_dict(self):
        try:
            contents = self.read_string()
            return json.loads(contents)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def write_json_dict(self, j_dict):
        self.write_string(json.JSONEncoder().encode(j_dict))

    def periodic_plan_to_json(self,plan):
        if plan.end_time is None:
            end_time = None
        else:
            end_time = plan.end_time.timestamp()
        period = plan.period
        if isinstance(period,dt.timedelta):
            period = period.total_seconds()
        result_dict = {PeriodicPlanAttributes.PERIOD: period,
                       PeriodicPlanAttributes.END_TIME: end_time,
                       PeriodicPlanAttributes.TASK_TEMPLATE: self.task_to_json(plan.task_template),
                       PeriodicPlanAttributes.TASK_ID: str(plan.task_id),
                       PeriodicPlanAttributes.UID: str(plan.uid),
                       PeriodicPlanAttributes.LAST_UPDATE_TIME: plan.last_update_time.timestamp(),
                       PeriodicPlanAttributes.USER: plan.user
                       }
        return result_dict

    def periodic_plan_from_json(self,j_dict):
        end_time = j_dict[PeriodicPlanAttributes.END_TIME]
        if end_time is not None:
            end_time = dt.datetime.fromtimestamp(end_time)
        if not isinstance(j_dict[PeriodicPlanAttributes.PERIOD], str):
            j_dict[PeriodicPlanAttributes.PERIOD] = dt.timedelta(seconds=j_dict[PeriodicPlanAttributes.PERIOD])
        j_dict[PeriodicPlanAttributes.END_TIME] = end_time
        j_dict[PeriodicPlanAttributes.TASK_TEMPLATE] = self.task_from_json(j_dict[PeriodicPlanAttributes.TASK_TEMPLATE])
        j_dict[PeriodicPlanAttributes.TASK_ID] = uuid.UUID(j_dict[PeriodicPlanAttributes.TASK_ID])
        j_dict[PeriodicPlanAttributes.LAST_UPDATE_TIME] = dt.datetime.fromtimestamp(j_dict[PeriodicPlanAttributes.LAST_UPDATE_TIME])
        j_dict[PeriodicPlanAttributes.UID] = uuid.UUID(j_dict[PeriodicPlanAttributes.UID])
        return PeriodicPlan(**j_dict)

    def periodic_plans_dict_to_json(self,plans_dict):
        j_dict = {}
        for k,v in plans_dict.items():
            j_dict[str(k)] = self.periodic_plan_to_json(v)
        return j_dict

    def periodic_plans_dict_from_json(self,j_dict):
        plans_dict = {}
        for k,v in j_dict.items():
            plans_dict[uuid.UUID(k)] = self.periodic_plan_from_json(v)
        return plans_dict
