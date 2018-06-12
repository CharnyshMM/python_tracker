"""Testcasses for PeriodicPlan class and Period"""

from lib.entities.plan import PeriodicPlan,Period
from lib.entities.task import Task,TaskAttributes
from lib.entities.exceptions import NoTimeValueError
import datetime as dt
import unittest


class PlanTestCase(unittest.TestCase):
    MINUTES_PERIOD = dt.timedelta(minutes=3)

    TITLE = 'title'
    AUTHOR = 'tester'
    FEBRUARY_29_2016 = dt.datetime(2016, 2, 29, 10, 0)
    MARCH_29_2016 = dt.datetime(2016, 3, 29, 10, 0)
    MARCH_31_2016 = dt.datetime(2016, 3, 31, 10, 0)
    MAY_1_2016 = dt.datetime(2016, 3, 31, 10, 0)
    MARCH_1_2018 = dt.datetime(2018, 3, 1, 10, 0)
    TIMEDELTA = dt.timedelta(hours=1)
    USER = 'user1'

    def setUp(self):
        self.minutes_task = Task(title=self.TITLE,
                                 author=self.AUTHOR,
                                 start_time=dt.datetime.now(),
                                 end_time=dt.datetime.now() + self.TIMEDELTA,
                                 can_edit=[self.USER])
        self.minutes_task_id = self.minutes_task.get_attribute(TaskAttributes.UID)

        self.year_task = Task('TEMPLATE', self.USER, start_time=self.FEBRUARY_29_2016,
                              remind_times=[self.FEBRUARY_29_2016 - self.TIMEDELTA,
                                            self.FEBRUARY_29_2016 + self.TIMEDELTA])
        self.year_task_id = self.year_task.get_attribute(TaskAttributes.UID)

    def tearDown(self):
        self.minutes_task = None
        self.minutes_task_id = None
        self.year_task = None
        self.year_task_id = None
        self.plan = None

    def test_no_start_time_check(self):
        task = Task(self.TITLE,self.AUTHOR)
        with self.assertRaises(NoTimeValueError):
            PeriodicPlan(Period.MONTHLY,task, task.get_attribute(TaskAttributes.UID),self.AUTHOR)

    def test_plan_update(self):
        plan = PeriodicPlan(period=self.MINUTES_PERIOD,
                            task_template=self.minutes_task,
                            task_id=self.minutes_task_id,
                            user=self.USER)
        plan.last_update_time = None
        self.assertTrue(plan.periodic_update_needed())
        next_task = plan.get_next_periodic_task()
        self.assertEqual(next_task.get_attribute(TaskAttributes.START_TIME),
                         self.minutes_task.get_attribute(TaskAttributes.START_TIME) + self.MINUTES_PERIOD)
        self.assertEqual(next_task.get_attribute(TaskAttributes.PLAN), plan.uid)

    def test_plan_stop(self):
        plan = PeriodicPlan(period=self.MINUTES_PERIOD,
                            task_template=self.minutes_task,
                            task_id=self.minutes_task_id,
                            user=self.USER)
        while plan.periodic_update_needed():
            plan.get_next_periodic_task()
        self.assertFalse(plan.periodic_update_needed())

    def test_year_period(self):
        plan = PeriodicPlan(Period.YEARLY, self.year_task, self.year_task_id, self.USER)
        self.assertTrue(plan.periodic_update_needed())

        plan.get_next_periodic_task()

        self.assertTrue(plan.periodic_update_needed())
        next_event = plan.get_next_periodic_task()

        next_task_start_time = next_event.get_attribute(TaskAttributes.START_TIME)
        self.assertEqual(next_task_start_time, self.MARCH_1_2018)

        reminders = next_event.get_attribute(TaskAttributes.REMIND_TIMES)
        expected_reminders = [self.MARCH_1_2018 + self.TIMEDELTA, self.MARCH_1_2018 - self.TIMEDELTA]
        self.assertCountEqual(reminders, expected_reminders)

    def test_month_period(self):
        plan = PeriodicPlan(Period.MONTHLY, self.year_task, self.year_task_id, self.USER)
        next_task = None
        previous_task = None
        while plan.periodic_update_needed():
            previous_task = next_task
            next_task = plan.get_next_periodic_task()

        start_time = next_task.get_attribute(TaskAttributes.START_TIME)
        previous_start_time = previous_task.get_attribute(TaskAttributes.START_TIME)
        future_delta = dt.datetime.now() - start_time
        tasks_delta = start_time - previous_start_time
        self.assertTrue(tasks_delta > future_delta >= dt.timedelta(0))




if __name__ == '__main__':
    unittest.main()