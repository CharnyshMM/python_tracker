from lib.entities.plan import PeriodicPlan
from lib.entities.task import Task, TaskAttributes
import datetime as dt
import unittest


class PlanTestCase(unittest.TestCase):
    PERIOD = dt.timedelta(minutes=3)
    START_DATE = dt.datetime.now()
    TIMEDELTA = dt.timedelta(minutes=5)

    TITLE = 'title'
    AUTHOR = 'tester'
    USER_1 = 'user_1'

    def setUp(self):
        self.task = Task(title=self.TITLE,
                         author=self.AUTHOR,
                         start_time=self.START_DATE,
                         end_time=self.START_DATE + self.TIMEDELTA,
                         can_edit=[self.USER_1]
                         )
        task_id = self.task.get_attribute(TaskAttributes.UID)
        self.plan_ = PeriodicPlan(period=self.PERIOD,
                                 task_template=self.task,
                                 task_id=task_id,
                                 user=self.USER_1)

    def tearDown(self):
        self.task = None
        self.plan = None

    def test_plan_update(self):
        self.plan.last_update_time = None
        self.assertTrue(self.plan.periodic_update_needed())
        next_task = self.plan.get_next_periodic_task()
        self.assertEqual(next_task.get_attribute(TaskAttributes.START_TIME),
                         self.task.get_attribute(TaskAttributes.START_TIME) + self.PERIOD)
        self.assertEqual(next_task.get_attribute(TaskAttributes.PLAN), self.plan.uid)

    def test_plan_stop(self):
        if self.plan.periodic_update_needed():
            self.plan.get_next_periodic_task()
        self.assertFalse(self.plan.periodic_update_needed())


if __name__ == '__main__':
    unittest.main()