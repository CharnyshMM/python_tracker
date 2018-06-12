import unittest
from lib.entities.tasks_manager import *
from lib.entities.exceptions import *
import datetime

class TasksManagerTestCase(unittest.TestCase):
    TITLE_1 = 'title'
    TITLE_2 = 'title 2'
    TITLE_3 = 'title 3'
    TITLE_4 = 'title 4'
    USER_1 = 'user_1'
    USER_2 = 'user_2'
    CHECK_TIME = datetime.datetime.now()
    TIMEDELTA = datetime.timedelta(minutes=30)

    def setUp(self):
        # setting up self.tasks_... for testing
        self.task_starts_at_check = Task(title=self.TITLE_1, author=self.USER_1, start_time=self.CHECK_TIME,
                                         end_time=self.CHECK_TIME + 4 * self.TIMEDELTA)
        self.task_starts_at_check_id = self.task_starts_at_check.get_attribute(TaskAttributes.UID)

        self.task_around_check = Task(title=self.TITLE_2, author=self.USER_2, start_time=self.CHECK_TIME - self.TIMEDELTA,
                                      end_time=self.CHECK_TIME + self.TIMEDELTA)
        self.task_around_check_id = self.task_around_check.get_attribute(TaskAttributes.UID)

        self.task_late = Task(title=self.TITLE_3, author=self.USER_1, start_time=self.CHECK_TIME + self.TIMEDELTA,
                              end_time=self.CHECK_TIME + 4 * self.TIMEDELTA, parent=self.task_starts_at_check_id)
        self.task_late_id = self.task_late.get_attribute(TaskAttributes.UID)

        self.task_ends_at_check = Task(title=self.TITLE_4, author=self.USER_2, start_time=self.CHECK_TIME - 10 * self.TIMEDELTA,
                                       end_time=self.CHECK_TIME - self.TIMEDELTA / 30)
        self.task_ends_at_check_id = self.task_ends_at_check.get_attribute(TaskAttributes.UID)

        # setting up self.tasks_manager
        self.tasks_manager = TasksManager({self.task_starts_at_check_id: self.task_starts_at_check,
                                           self.task_around_check_id: self.task_around_check})
        self.tasks_manager.create_new_task(self.task_late, self.USER_1)
        self.tasks_manager.create_new_task(self.task_ends_at_check, self.USER_2)
        self.task_ends_at_check.add_to_attribute(TaskAttributes.REMIND_TIMES, self.CHECK_TIME + self.TIMEDELTA / 30,
                                                 self.USER_2)
        self.task_starts_at_check.add_to_attribute(TaskAttributes.REMIND_TIMES,
                                                   [self.CHECK_TIME - self.TIMEDELTA,
                                                    self.CHECK_TIME + self.TIMEDELTA / 30], self.USER_1)

    def tearDown(self):
        self.task_starts_at_check = None
        self.task_around_check = None
        self.task_starts_at_check_id = None
        self.task_around_check_id = None
        self.tasks_manager = None

    def test_create_task(self):
        self.assertListEqual(self.task_starts_at_check.get_attribute(TaskAttributes.SUBTASKS), [self.task_late_id])
        self.task_late.set_attribute(TaskAttributes.PARENT, self.task_around_check_id, self.USER_1)
        with self.assertRaises(EndTimeOverflowError):
            self.tasks_manager.create_new_task(self.task_late, self.USER_2)

    def test_remove_task(self):
        self.tasks_manager.remove_task(self.task_late_id, self.USER_1)
        self.assertEqual(self.task_starts_at_check.try_get_attribute(TaskAttributes.SUBTASKS), None)

    def test_remove_with_subtasks(self):
        with self.assertRaises(SubtasksNotRemovedError):
            self.tasks_manager.remove_task(self.task_starts_at_check_id, self.USER_1)
        self.tasks_manager.remove_with_subtasks(self.task_starts_at_check_id, self.USER_1)

        self.assertEqual(self.task_starts_at_check.try_get_attribute(TaskAttributes.SUBTASKS), None)

    def test_find(self):
        two_tasks = self.tasks_manager.find_task(attributes={TaskAttributes.AUTHOR:self.USER_1})

        self.assertDictEqual(two_tasks, {self.task_starts_at_check_id: self.task_starts_at_check, self.task_late_id: self.task_late})

    def test_select_actual_tasks(self):
        actuals = self.tasks_manager.select_actual_tasks(time=self.CHECK_TIME)
        self.assertDictEqual(actuals['continuing'], {self.task_around_check_id: self.task_around_check})
        self.assertDictEqual(actuals['starting'], {self.task_starts_at_check_id: self.task_starts_at_check})
        self.assertDictEqual(actuals['ending'], {self.task_ends_at_check_id: self.task_ends_at_check})

    def test_select_actual_reminders(self):
        reminders = self.tasks_manager.select_actual_reminders(self.CHECK_TIME)
        self.assertCountEqual(reminders, [self.task_ends_at_check, self.task_starts_at_check])


if __name__ == '__main__':
    unittest.main()