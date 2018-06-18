import unittest
import datetime as dt
from lib.interface import Interface
from lib.entities.task import Task, TaskAttributes, TaskStatus
from lib.db_adapter import DBAdapter


class DBEmulator(DBAdapter):
    def __init__(self):
        self.tasks_storage = {}
        self.plans_storage = {}

    def get_all_tasks(self):
        return self.tasks_storage

    def put_all_tasks(self, tasks_collection):
        self.tasks_storage = tasks_collection

    def get_all_plans(self):
        return self.plans_storage

    def put_all_plans(self, plans_dict):
        self.plans_storage = plans_dict

class InterfaceTestCase(unittest.TestCase):
    TITLE_1 = 'title'
    TITLE_2 = 'title 2'
    TITLE_3 = 'title 3'
    TITLE_4 = 'title 4'
    USER_1 = 'user_1'
    USER_2 = 'user_2'
    CHECK_TIME = dt.datetime.now()
    TIMEDELTA = dt.timedelta(minutes=30)

    def setUp(self):
        self.task_starts_at_check = Task(title=self.TITLE_1, author=self.USER_1, start_time=self.CHECK_TIME,
                                         end_time=self.CHECK_TIME + 4 * self.TIMEDELTA)
        self.task_starts_at_check_id = self.task_starts_at_check.get_attribute(TaskAttributes.UID)

        self.task_around_check = Task(title=self.TITLE_2, author=self.USER_2,
                                      start_time=self.CHECK_TIME - self.TIMEDELTA,
                                      end_time=self.CHECK_TIME + self.TIMEDELTA)
        self.task_around_check_id = self.task_around_check.get_attribute(TaskAttributes.UID)


        self.db_emulator = DBEmulator()
        self.db_emulator.tasks_storage = {self.task_starts_at_check_id: self.task_starts_at_check,
                                          self.task_around_check_id: self.task_around_check}

        self.interface = Interface(self.db_emulator, self.USER_1)


    def tearDown(self):
        self.task_starts_at_check = None
        self.task_starts_at_check_id = None
        self.task_around_check = None
        self.task_around_check_id = None
        self.task_late = None
        self.task_late_id = None
        self.task_ends_at_check = None
        self.task_ends_at_check_id = None
        self.interface = None
        self.db_emulator = None

    def test_add_task(self):
        task_id = self.interface.create_task(title=self.TITLE_3, start_time=self.CHECK_TIME + self.TIMEDELTA)
        self.assertTrue(task_id in self.db_emulator.tasks_storage)

    def test_db_equalty_task(self):
        self.assertDictEqual(self.db_emulator.tasks_storage, self.interface.tasks_manager.tasks)
        self.assertDictEqual(self.db_emulator.plans_storage, self.interface.plans_manager.plans)

    def test_check_time(self):
        actuals, reminders = self.interface.check_time(self.CHECK_TIME)
        self.assertDictEqual(actuals['continuing'], {self.task_around_check_id: self.task_around_check})
        self.assertDictEqual(actuals['starting'], {self.task_starts_at_check_id: self.task_starts_at_check})
        self.assertDictEqual(actuals['ending'], {})

    def test_complete_task(self):
        self.interface.complete_task(self.task_starts_at_check_id)
        status = self.interface.get_task(self.task_starts_at_check_id).get_attribute(TaskAttributes.STATUS)
        self.assertTrue(status == TaskStatus.COMPLETE)


if __name__ == '__main__':
    unittest.main()