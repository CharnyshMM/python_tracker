from lib.task import *
import unittest


class TaskTestCase(unittest.TestCase):
    TITLE = 'title'
    AUTHOR = 'tester'
    USER_1 = 'user_1'
    USER_2 = 'user_2'
    START_DATE = datetime.datetime.now()
    TIMEDELTA = datetime.timedelta(minutes=10)

    def setUp(self):
        self.task = Task(title=self.TITLE,
                         author=self.AUTHOR,
                         start_date=self.START_DATE,
                         end_date=self.START_DATE + 2*self.TIMEDELTA)

    def tearDown(self):
        self.task = None

    def test_who_can_edit_task(self):
        with self.assertRaises(PermissionError):
            self.task.add_to_attribute(attr=TaskAttributes.CAN_EDIT,
                                   val=self.USER_1,
                                   user=self.USER_1)

    def test_try_get_attribute(self):
        self.assertIsNone(self.task.try_get_attribute(TaskAttributes.SUBTASKS))
        self.assertIs(self.task.try_get_attribute(TaskAttributes.TITLE),self.TITLE)


if __name__ == '__main__':
    unittest.main()