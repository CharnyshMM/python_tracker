import datetime as dt
import calendar
import copy
from lib.task import TaskAttributes
from uuid import uuid1
from lib.exceptions import NoTimeValueError




class PeriodicPlanAttributes:
    PERIOD = 'period'
    END_TIME = 'end_time'
    TASK_ID = 'task_id'
    UID = 'uid'
    TASK_TEMPLATE = 'task_template'
    USER = 'user'
    LAST_UPDATE_TIME = 'last_update_time'


class Period:
    YEARLY = 'yearly'
    MONTHLY = 'monthly'
    WEEKLY = 'weekly'
    DAILY = 'daily'

    @classmethod
    def add_timedelta(cls,period, offset_date):
        if isinstance(period,dt.timedelta):
            return offset_date + period
        if period == cls.DAILY:
            return offset_date + dt.timedelta(days=1)
        if period == cls.WEEKLY:
            return offset_date + dt.timedelta(weeks=1)
        if period == cls.MONTHLY:
            month = offset_date.month
            day = offset_date.day
            year = offset_date.year
            if month < 12:
                month += 1
            else:
                month = 1
                year += 1
            month_range = calendar.monthrange(year,month)[1]
            if day <= month_range:
                return dt.datetime(year=year,month=month, day=day,hour=offset_date.hour, minute=offset_date.minute)
            if month < 12:
                month += 1
            else:
                month = 1
                year += 1
            day = day - month_range
            return dt.datetime(year=year, month=month, day=day, hour=offset_date.hour, minute=offset_date.minute)
        if period == Period.YEARLY:
            year = offset_date.year
            year += 1
            return dt.datetime(year=year, month=offset_date.month, day=offset_date.day, hour=offset_date.hour, minute=offset_date.minute)
        raise ValueError('unknown period')

class PeriodicPlan:
    def __init__(self, period, task_template, task_id, user, uid=None, end_time=None, last_update_time = None):
        self.period = period
        self.task_template = copy.copy(task_template)
        if self.task_template.try_get_attribute(TaskAttributes.START_TIME) is None:
            raise NoTimeValueError
        self.task_id = task_id
        self.user = user
        if uid is not None:
            self.uid = uid
        else:
            self.uid = uuid1()
        self.task_template.set_attribute(TaskAttributes.PLAN, self.uid, user)
        self.end_time = end_time
        self.last_update_time = last_update_time

    def get_next_periodic_task(self):
        start_time = self.task_template.try_get_attribute(TaskAttributes.START_TIME)
        remind_times = self.task_template.try_get_attribute(TaskAttributes.REMIND_TIMES)
        end_time = self.task_template.try_get_attribute(TaskAttributes.END_TIME)

        new_task = copy.copy(self.task_template)

        start_time = Period.add_timedelta(self.period, start_time)
        if end_time is not None:
            end_time = Period.add_timedelta(self.period, end_time)

        if remind_times is not None:
            for i in range(len(remind_times)):
                remind_times[i] = Period.add_timedelta(self.period,remind_times[i])
            new_task.set_attribute(TaskAttributes.REMIND_TIMES, remind_times, self.user)

        new_task.set_attribute(TaskAttributes.START_TIME, start_time, self.user)
        new_task.set_attribute(TaskAttributes.END_TIME, end_time, self.user)
        new_task.attributes[TaskAttributes.UID] = uuid1()
        self.task_template = copy.copy(new_task)
        self.last_update_time = start_time

        return new_task

    def periodic_update_needed(self):
        if self.last_update_time is None:
            return True
        if self.end_time is not None:
            if dt.datetime.now() > self.end_time:
                return False
        delta = dt.datetime.now() - Period.add_timedelta(self.period, self.last_update_time)
        if delta >= dt.timedelta(0):
            return True
        return False

