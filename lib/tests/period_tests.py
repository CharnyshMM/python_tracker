"""This module has tests for Period class from plan module"""

import unittest
import datetime as dt
from lib.entities.plan import  PeriodicPlan, Period
from lib.entities.task import Task,TaskAttributes

class PeriodTestCase(unittest.TestCase):
    FEBRUARY_29_2016 = dt.datetime(2016, 2, 29, 10, 0)
    MARCH_29_2016 = dt.datetime(2016,3,29,10,0)
    MARCH_31_2016 = dt.datetime(2016, 3, 31, 10, 0)
    MAY_1_2016 = dt.datetime(2016, 3, 31, 10, 0)
    MARCH_1_2017 = dt.datetime(2017, 3, 1, 10, 0)
    TIMEDELTA = dt.timedelta(hours=1)
    USER = 'user1'

    def setUp(self):
        self.task = TASK_TEMPLATE = Task('TEMPLATE', self.USER, start_time=self.FEBRUARY_29_2016,
                                         remind_times=[self.FEBRUARY_29_2016 - self.TIMEDELTA,
                                                       self.FEBRUARY_29_2016 + self.TIMEDELTA])
        self.task_id = self.task.get_attribute(TaskAttributes.UID)

    def tearDown(self):
        self.task = None
        self.task_id = None

    def test_year_period(self):
        plan = PeriodicPlan(Period.YEARLY, self.task, self.task_id, self.USER)
        self.assertTrue(plan.periodic_update_needed())

        next_event = plan.get_next_periodic_task()
        next_task_start_time = next_event.get_attribute(TaskAttributes.START_TIME)
        self.assertEqual(next_task_start_time, self.MARCH_1_2017)

        reminders = next_event.get_attribute(TaskAttributes.REMIND_TIMES)
        expected_reminders = [self.MARCH_1_2017 + self.TIMEDELTA, self.MARCH_1_2017 - self.TIMEDELTA]
        self.assertCountEqual(reminders, expected_reminders)

    def text_month_period(self):
        pass
