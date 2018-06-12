from lib.entities.plan import PeriodicPlan,Period
from lib.entities.plans_manager import PlansManager
from lib.entities.task import Task, TaskAttributes
import datetime as dt
import unittest


class PlanTestCase(unittest.TestCase):

    TITLE = 'title'
    AUTHOR = 'tester'
    USER_1 = 'user_1'
    MINUTES_DELTA = dt.timedelta(minutes=10)
    DAY_DELTA = dt.timedelta(days=1)

    def setUp(self):
        self.plans_manager = PlansManager()
        self.minutes_task_start_time = start_time = dt.datetime.now()
        self.minutes_task = Task(self.TITLE+"min", self.AUTHOR, start_time=self.minutes_task_start_time)
        self.minutes_task_id = self.minutes_task.get_attribute(TaskAttributes.UID)
        self.minutes_plan = PeriodicPlan(self.MINUTES_DELTA, self.minutes_task, self.minutes_task_id, self.AUTHOR)
        self.plans_manager.add_plan(self.minutes_plan)

        self.day_task_start_time = start_time=dt.datetime.now() - 4 * self.DAY_DELTA
        self.day_task = Task(self.TITLE+"day", self.AUTHOR, start_time=self.day_task_start_time)
        self.day_task_id = self.day_task.get_attribute(TaskAttributes.UID)
        self.day_plan = PeriodicPlan(self.DAY_DELTA, self.day_task, self.day_task_id, self.AUTHOR,
                                     end_time=self.day_task_start_time + 2*self.DAY_DELTA)
        self.plans_manager.add_plan(self.day_plan)

    def tearDown(self):
        self.plans_manager = None
        self.day_task = None
        self.day_task_id = None
        self.day_plan = None
        self.minutes_plan = None
        self.minutes_task_id = None
        self.minutes_task = None

    def test_get_updates(self):
        updates = self.plans_manager.get_updates()

        day_forward = Period.add_timedelta(self.DAY_DELTA, self.day_task_start_time)
        two_days_forward = Period.add_timedelta(self.DAY_DELTA, day_forward)

        minutes_forward = Period.add_timedelta(self.MINUTES_DELTA,self.minutes_task_start_time)

        minutes_task_correct = False
        day_1_task_correct = False
        day_2_task_correct = False
        unknown = False
        for task in updates:
            if task.get_attribute(TaskAttributes.START_TIME) == minutes_forward:
                minutes_task_correct = True
            elif task.get_attribute(TaskAttributes.START_TIME) == day_forward:
                day_1_task_correct = True
            elif task.get_attribute(TaskAttributes.START_TIME) == two_days_forward:
                day_2_task_correct = True
            else:
                unknown = True
        self.assertFalse(unknown)
        self.assertTrue(minutes_task_correct and day_1_task_correct and day_2_task_correct)






if __name__ == '__main__':
    unittest.main()