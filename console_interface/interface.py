from lib.tasks_manager import *
from lib.plan import *
from lib.plans_manager import PlansManager
from lib.logger import *
from json_db.interface import DB


class Interface:
    @log_decorator
    def __init__(self, user):
        configure_logger()
        self.current_user = user
        self.db = DB()
        self.tasks_manager = TasksManager(tasks=self.db.get_all_tasks())
        self.plans_manager = PlansManager(self.db.get_all_plans())


    @log_decorator
    def add_task(self, title, start_date=None, end_date=None, remind_dates=None, status=TaskStatus.ACTIVE, owned_by=None,
                 subtasks=None, tags=None, can_edit=None, priority=TaskPriority.MEDIUM):

        t = Task(title,self.current_user,start_date=start_date,end_date=end_date,remind_dates=remind_dates,status=status,
                 priority=priority, owned_by=owned_by,subtasks=subtasks,tags=tags,can_edit=can_edit)
        self.tasks_manager.create_new_task(t,self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)

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
    def edit_task(self, task_id, title=None, author=None, start_date=None,
                  end_date=None, remind_dates=None, owned_by=None, subtasks=None, tags=None, can_edit=None, status=None, ):
        params_dict = {}
        if title is not None:
            params_dict[TaskAttributes.TITLE] = title
        if author is not None:
            params_dict[TaskAttributes.AUTHOR] = author
        if start_date is not None:
            params_dict[TaskAttributes.START_DATE] = start_date
        if end_date is not None:
            params_dict[TaskAttributes.END_DATE] = end_date
        if remind_dates is not None:
            params_dict[TaskAttributes.REMIND_DATES] = remind_dates
        if owned_by is not None:
            params_dict[TaskAttributes.OWNED_BY] = owned_by
        if subtasks is not None:
            params_dict[TaskAttributes.SUBTASKS] = subtasks
        if tags is not None:
            params_dict[TaskAttributes.TAGS] = tags
        self.tasks_manager.edit_task(task_id, params_dict, self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)

    @log_decorator
    def task_set_attribute(self,task_id, attribute, value):
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
    def find_tasks(self, title=None, author=None, start_date=None,
                   end_date=None, remind_dates=None, owned_by=None, subtasks=None, tags=None, can_edit=None, status=None, ):
        attributes = {}
        if title is not None:
            attributes[TaskAttributes.TITLE] = title
        if author is not None:
            attributes[TaskAttributes.AUTHOR] = author
        if start_date is not None:
            attributes[TaskAttributes.START_DATE] = start_date
        if end_date is not None:
            attributes[TaskAttributes.END_DATE] = end_date
        if remind_dates is not None:
            attributes[TaskAttributes.REMIND_DATES] = remind_dates
        if owned_by is not None:
            attributes[TaskAttributes.OWNED_BY] = owned_by
        if subtasks is not None:
            attributes[TaskAttributes.SUBTASKS] = subtasks
        if tags is not None:
            attributes[TaskAttributes.TAGS] = tags
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
    def add_periodic_plan(self,period, task_template, task_id, end_date):
        plan = PeriodicPlan(period,task_template,task_id, self.current_user,end_date=end_date)
        self.plans_manager.add_plan(plan)
        self.check_plans()

    @log_decorator
    def rm_periodic_plan(self,plan_id):
        self.plans_manager.remove_plan(plan_id)
        self.db.put_all_plans(self.plans_manager.plans)

    @log_decorator
    def check_plans(self):
        new_tasks = self.plans_manager.get_updates()
        for task in new_tasks:
            self.tasks_manager.create_new_task(task, self.current_user)
        self.db.put_all_tasks(self.tasks_manager.tasks)
        self.db.put_all_plans(self.plans_manager.plans)