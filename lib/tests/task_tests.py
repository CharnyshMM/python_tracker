from lib.entities.task import *
import unittest
import datetime

class TaskTestCase(unittest.TestCase):
    TITLE = 'title'
    AUTHOR = 'tester'
    USER_1 = 'user_1'
    USER_2 = 'user_2'
    START_DATE = datetime.datetime.now()
    TIMEDELTA = datetime.timedelta(minutes=10)

    def setUp(self):
        self.task = Task(title=self.TITLE, author=self.AUTHOR, start_time=self.START_DATE,
                         end_time=self.START_DATE + 4 * self.TIMEDELTA)

    def tearDown(self):
        self.task = None

    def test_who_can_edit_task(self):
        with self.assertRaises(PermissionError):
            self.task.add_to_attribute(attr=TaskAttributes.CAN_EDIT, val=self.USER_1, user=self.USER_1)
        with self.assertRaises(ValueError):
            t = Task(title=self.TITLE, author=self.AUTHOR, start_time=self.START_DATE + 2 * self.TIMEDELTA,
                     end_time=self.START_DATE)

    def test_setting_attributes(self):
        self.task.set_attribute(attr=TaskAttributes.STATUS, val=TaskStatus.COMPLETE, user=self.AUTHOR)
        self.assertEqual(self.task.get_attribute(TaskAttributes.STATUS),TaskStatus.COMPLETE)

    def test_adding_to_attributes(self):
        self.task.add_to_attribute(TaskAttributes.REMIND_TIMES, self.START_DATE + self.TIMEDELTA, self.AUTHOR)
        self.task.add_to_attribute(TaskAttributes.REMIND_TIMES, self.START_DATE + 2 * self.TIMEDELTA, self.AUTHOR)
        self.task.add_to_attribute(TaskAttributes.CAN_EDIT, self.USER_1, self.AUTHOR)
        self.assertListEqual(self.task.get_attribute(TaskAttributes.REMIND_TIMES),
                             [self.START_DATE + self.TIMEDELTA, self.START_DATE + 2 * self.TIMEDELTA])
        self.task.remove_from_attribute(TaskAttributes.REMIND_TIMES, self.START_DATE + 2 * self.TIMEDELTA, self.USER_1)
        self.assertListEqual(self.task.get_attribute(TaskAttributes.REMIND_TIMES),
                             [self.START_DATE + self.TIMEDELTA], self.USER_1)

    def test_try_get_attribute(self):
        self.assertIsNone(self.task.try_get_attribute(TaskAttributes.SUBTASKS))
        self.assertIs(self.task.try_get_attribute(TaskAttributes.TITLE),self.TITLE)



if __name__ == '__main__':
    unittest.main()