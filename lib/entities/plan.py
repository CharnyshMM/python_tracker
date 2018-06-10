r"""
        This Module contains classes describing single plan.
"""

import datetime as dt
import calendar
import copy
from lib.entities.task import TaskAttributes
from uuid import uuid1
from lib.entities.exceptions import NoTimeValueError




class PeriodicPlanAttributes:
    r"""
       Lists all the attributes of a single Plan.
       PERIOD - a period to repeat planned task
       END_TIME - when to stop repeating plan( if None then never stop)
       TASK_ID - id of planned task
       TASK_TEMPLATE - a Task object to be a template for each task created automatically by Plan
       USER - a user who has rights to edit the TaskTemlpate
       LAST_UPDATE_TIME - when last task was created by this Plan
    """
    PERIOD = 'period'
    END_TIME = 'end_time'
    TASK_ID = 'task_id'
    UID = 'uid'
    TASK_TEMPLATE = 'task_template'
    USER = 'user'
    LAST_UPDATE_TIME = 'last_update_time'


class Period:
    r"""
    Period class is for dealing with period for PeriodicPlan
    It provides string representations of fised Periods:
        YEARLY
        MONTHLY
        WEEKLY
        DAILY
    And the add_timedelta functions that takes a date, adds a period value to it and returns the result
    """
    YEARLY = 'yearly'
    MONTHLY = 'monthly'
    WEEKLY = 'weekly'
    DAILY = 'daily'

    @classmethod
    def add_timedelta(cls,period, offset_date):
        r"""
        Function to make a periodic move.

        :param period: datetime.timedelta object or one of string periods provided by this class
        :param offset_date: datetime.datetime date to add a period to
        :return: datetime.datetime new date object that represents offset_date + period
        """
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
            month = offset_date.month
            day = offset_date.day
            non_leap_year_issue = (month == 2 and day == 29 and calendar.monthrange(year,month)[1] == 28)
            if non_leap_year_issue:
                month = 3
                day = 1
            return dt.datetime(year=year, month=month, day=day, hour=offset_date.hour, minute=offset_date.minute)
        raise ValueError('unknown period')


class PeriodicPlan:

    r"""
        The core class for dealing with plans.
        Its instance describes a plan with:
            - template of periodic task
            - period of repetition
            - last update time
            - user, who can edit the task template
        The instance could say if it needs an update and perform an update, returning new task
        """

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
        r"""
            Function to create and return next periodic task made of task_template.
            ! It doesn't check whether it needs to update or not, it just returns a new task moved a period ahead!
        :return: Task - next periodic task
        """

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
        """
            Fucntion to check if it's time to update a periodic task.
        :return: Boolean True - if update is needed, otherwise False
        """
        if self.last_update_time is None:
            return True
        if self.end_time is not None:
            if dt.datetime.now() > self.end_time:
                return False
        delta = dt.datetime.now() - Period.add_timedelta(self.period, self.last_update_time)
        if delta >= dt.timedelta(0):
            return True
        return False

