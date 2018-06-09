import unittest
from lib.tasks_manager import *
from lib.exceptions import *


class TasksManagerTestCase(unittest.TestCase):
    TITLE_1 = 'title'
    TITLE_2 = 'title2'
    TITLE_3 = 'title3'
    TITLE_4 = 'title4'
    USER_1 = 'user_1'
    USER_2 = 'user_2'
    START_DATE = datetime.datetime.now()
    TIMEDELTA = datetime.timedelta(minutes=30)

    def setUp(self):
        self.task1 = Task(title=self.TITLE_1, author=self.USER_1, start_time=self.START_DATE,
                          end_time=self.START_DATE + 4 * self.TIMEDELTA)
        self.task2 = Task(title=self.TITLE_2, author=self.USER_2, start_time=self.START_DATE - self.TIMEDELTA,
                          end_time=self.START_DATE+self.TIMEDELTA)
        self.task1_id = self.task1.get_attribute(TaskAttributes.UID)
        self.task2_id = self.task2.get_attribute(TaskAttributes.UID)
        self.tasks_manager = TasksManager({self.task1_id: self.task1, self.task2_id: self.task2})
        self.task3 = Task(title=self.TITLE_3, author=self.USER_1, start_time=self.START_DATE + self.TIMEDELTA,
                          end_time=self.START_DATE + 4 * self.TIMEDELTA, parent=self.task1_id)
        self.task3_id = self.task3.get_attribute(TaskAttributes.UID)
        self.task4 = Task(title=self.TITLE_4, author=self.USER_2, start_time=self.START_DATE - 10*self.TIMEDELTA,
                          end_time=self.START_DATE - self.TIMEDELTA/30)
        self.task4_id = self.task4.get_attribute(TaskAttributes.UID)


    def tearDown(self):
        self.task1 = None
        self.task2 = None
        self.task1_id = None
        self.task2_id = None
        self.tasks_manager = None

    def test_create_task(self):
        self.tasks_manager.create_new_task(self.task3, self.USER_1)
        self.assertListEqual(self.task1.get_attribute(TaskAttributes.SUBTASKS),[self.task3_id])
        self.task3.set_attribute(TaskAttributes.PARENT, self.task2_id, self.USER_1)
        with self.assertRaises(EndTimeOverflowError):
            self.tasks_manager.create_new_task(self.task3,self.USER_2)

    def test_remove_task(self):
        self.tasks_manager.create_new_task(self.task3, self.USER_1)
        self.tasks_manager.remove_task(self.task3_id, self.USER_1)
        self.assertEqual(self.task1.try_get_attribute(TaskAttributes.SUBTASKS),None)

    def test_remove_with_subtasks(self):
        self.tasks_manager.create_new_task(self.task3, self.USER_1)
        with self.assertRaises(SubtasksNotRemovedError):
            self.tasks_manager.remove_task(self.task1_id, self.USER_1)
        self.tasks_manager.remove_with_subtasks(self.task1_id, self.USER_1)
        self.assertEqual(self.task1.try_get_attribute(TaskAttributes.SUBTASKS), None)

    def test_find(self):
        self.tasks_manager.create_new_task(self.task3, self.USER_1)
        self.tasks_manager.create_new_task(self.task3, self.USER_1)
        two_tasks = self.tasks_manager.find_task(attributes={TaskAttributes.AUTHOR:self.USER_1})
        self.assertDictEqual(two_tasks,{self.task1_id: self.task1, self.task3_id: self.task3})

    def test_select_actuals(self):
        self.tasks_manager = TasksManager({self.task1_id: self.task1, self.task2_id: self.task2})
        self.tasks_manager.create_new_task(self.task3, self.USER_1)
        self.tasks_manager.create_new_task(self.task4, self.USER_2)
        self.task4.add_to_attribute(TaskAttributes.REMIND_TIMES,self.START_DATE + self.TIMEDELTA/30, self.USER_2)
        self.task1.add_to_attribute(TaskAttributes.REMIND_TIMES,
                                    [self.START_DATE-self.TIMEDELTA, self.START_DATE+self.TIMEDELTA/30],self.USER_1)
        actuals = self.tasks_manager.select_actual_tasks(time=self.START_DATE)
        self.assertDictEqual(actuals['continuing'], {self.task2_id: self.task2})
        self.assertDictEqual(actuals['starting'], {self.task1_id: self.task1})
        self.assertDictEqual(actuals['ending'],{self.task4_id: self.task4})
        reminders = self.tasks_manager.select_actual_reminders(self.START_DATE)
        self.assertListEqual(reminders,[self.task4,self.task1])


if __name__ == '__main__':
    unittest.main()