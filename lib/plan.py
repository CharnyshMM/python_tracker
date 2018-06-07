import datetime as dt
import copy
from lib.task import TaskAttributes
from uuid import uuid1


class PeriodicPlanAttributes:
    PERIOD = 'period'
    END_DATE = 'end_date'
    TASK_ID = 'task_id'
    UID = 'uid'
    TASK_TEMPLATE = 'task_template'
    USER = 'user'
    LAST_UPDATE_TIME = 'last_update_time'

class PeriodicPlan:
    def __init__(self, period, task_template, task_id, user, uid=None, end_date=None, last_update_time = None):
        self.period = period
        self.task_template = copy.copy(task_template)

        self.task_id = task_id
        self.user = user
        if uid is not None:
            self.uid = uid
        else:
            self.uid = uuid1()
        self.task_template.set_attribute(TaskAttributes.PLAN, self.uid, user)
        self.end_date = end_date
        self.last_update_time = last_update_time

    def get_next_periodic_task(self):
        start_date = self.task_template.try_get_attribute(TaskAttributes.START_DATE)
        remind_dates = self.task_template.try_get_attribute(TaskAttributes.REMIND_DATES)
        end_date = self.task_template.try_get_attribute(TaskAttributes.END_DATE)

        new_task = copy.copy(self.task_template)

        start_date += self.period
        end_date += self.period

        if remind_dates is not None:
            for i in range(len(remind_dates)):
                remind_dates[i] += self.period
            new_task.set_attribute(TaskAttributes.REMIND_DATES, remind_dates, self.user)

        new_task.set_attribute(TaskAttributes.START_DATE,start_date,self.user)
        new_task.set_attribute(TaskAttributes.END_DATE,end_date,self.user)
        new_task.attributes[TaskAttributes.UID] = uuid1()
        self.task_template = copy.copy(new_task)
        self.last_update_time = start_date

        return new_task

    def periodic_update_needed(self):
        if self.last_update_time is None:
            return True
        if self.end_date is not None:
            if dt.datetime.now() > self.end_date:
                return False
        delta = dt.datetime.now() - self.last_update_time
        if delta >= self.period:
            return True
        return False








