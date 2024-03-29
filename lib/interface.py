"""This module contains single Interface class"""

from lib.entities.tasks_manager import *
from lib.entities.plan import *
from lib.entities.plans_manager import PlansManager
from lib.logger import log_decorator


class Interface:
    """

    Interface class is designed to unite and encapsulate all the tasks and plans processing operations
    and provide convenient interface to operate with commands

    """

    @log_decorator
    def __init__(self, db_adapter, user):
        self.current_user = user
        self.db = db_adapter
        self.tasks_manager = TasksManager(tasks=self.db.get_all_tasks())
        self.plans_manager = PlansManager(self.db.get_all_plans())

    @log_decorator
    def create_task(self, title, start_time=None, end_time=None, remind_times=None, status=None, parent=None,
                    subtasks=None, tags=None, can_edit=None, priority=None):
        if priority is None:
            priority = TaskPriority.MEDIUM
        if status is None:
            status = TaskStatus.ACTIVE
        t = Task(title, self.current_user, start_time=start_time, end_time=end_time, remind_times=remind_times, status=status,
                 priority=priority, parent=parent, subtasks=subtasks, tags=tags, can_edit=can_edit)
        self.tasks_manager.add_new_task(t, self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)
        return t.get_attribute(TaskAttributes.UID)

    @log_decorator
    def add_task(self, new_task):
        self.tasks_manager.add_new_task(new_task, self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)
        return new_task.get_attribute(TaskAttributes.UID)

    @log_decorator
    def remove_task(self, task_id):
        self.tasks_manager.remove_task(task_id,self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)

    @log_decorator
    def remove_with_subtasks(self,task_id):
        self.tasks_manager.remove_with_subtasks(task_id, self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)

    @log_decorator
    def get_task(self, task_id):
        return self.tasks_manager.get_task(task_id)

    @log_decorator
    def task_set_attribute(self,task_id, attribute, value):
        if attribute == TaskAttributes.END_TIME:
            self.tasks_manager.edit_task_end_time(task_id,value,self.current_user)
        elif attribute == TaskAttributes.START_TIME:
            self.tasks_manager.edit_task_start_time(task_id,value,self.current_user)
        else:
            task = self.tasks_manager.get_task(task_id)
            task.set_attribute(attribute, value, self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)

    @log_decorator
    def task_add_attribute(self, task_id, attribute, value):
        task = self.tasks_manager.get_task(task_id)
        task.add_to_attribute(attribute, value, self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)

    @log_decorator
    def task_remove_attribute(self, task_id, attribute, value):
        task = self.tasks_manager.get_task(task_id)
        task.remove_from_attribute(attribute, value, self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)

    @log_decorator
    def find_tasks(self, title=None, author=None, start_time=None, end_time=None, remind_times=None, parent=None,
                   subtasks=None, tags=None, can_edit=None, status=None, priority=None, plan=None):

        """This method tries to find a task or tasks by passed parameters.
        returns a dict of tashs"""

        attributes = {}
        if title is not None:
            attributes[TaskAttributes.TITLE] = title
        if author is not None:
            attributes[TaskAttributes.AUTHOR] = author
        if start_time is not None:
            attributes[TaskAttributes.START_TIME] = start_time
        if end_time is not None:
            attributes[TaskAttributes.END_TIME] = end_time
        if remind_times is not None:
            attributes[TaskAttributes.REMIND_TIMES] = remind_times
        if parent is not None:
            attributes[TaskAttributes.PARENT] = parent
        if subtasks is not None:
            attributes[TaskAttributes.SUBTASKS] = subtasks
        if tags is not None:
            attributes[TaskAttributes.TAGS] = tags
        if priority is not None:
            attributes[TaskAttributes.PRIORITY] = priority
        if status is not None:
            attributes[TaskAttributes.STATUS] = status
        if can_edit is not None:
            attributes[TaskAttributes.CAN_EDIT] = can_edit
        if plan is not None:
            attributes[TaskAttributes.PLAN] = plan
        return self.tasks_manager.find_task(attributes)

    @log_decorator
    def get_all_tasks(self):
        return self.tasks_manager.get_all_tasks()

    @log_decorator
    def check_time(self, date,delta=None):
        self.check_plans()
        reminders = self.tasks_manager.select_actual_reminders(date,delta)
        actual_tasks = self.tasks_manager.select_actual_tasks(date,delta)
        return actual_tasks, reminders

    @log_decorator
    def add_periodic_plan(self, period, task_template, task_id, end_time):
        plan = PeriodicPlan(period, task_template, task_id, self.current_user, end_time=end_time)
        self.plans_manager.add_plan(plan)
        self.check_plans()

    @log_decorator
    def rm_periodic_plan(self,plan_id):
        self.plans_manager.remove_plan(plan_id)
        self.db.put_all_plans(self.plans_manager.plans)

    @log_decorator
    def get_plans_by_task_id(self, task_id):
        return self.plans_manager.find_plans_for_task(task_id)

    @log_decorator
    def check_plans(self):
        new_tasks = self.plans_manager.get_updates()
        for task in new_tasks:
            self.tasks_manager.add_new_task(task, task.get_attribute(TaskAttributes.AUTHOR))
        self.db.put_all_tasks(self.tasks_manager.tasks)
        self.db.put_all_plans(self.plans_manager.plans)

    @log_decorator
    def complete_task(self,task_id):
        task = self.tasks_manager.get_task(task_id)
        task.set_attribute(TaskAttributes.STATUS, TaskStatus.COMPLETE, self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)