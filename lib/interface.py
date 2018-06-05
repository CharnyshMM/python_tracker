from lib.tasks_manager import *
from lib.decorators import *
from lib.logger import *
from json_db.interface import DB

class Interface:
    def __init__(self, user):
        configure_logger()
        self.current_user = user
        self.db = DB()
        self.tasks_manager = TasksManager(self.db, user=user)
        try:
            self.tasks_manager.initialise_from_DB()
        except Exception :
            pass

    @log_decorator
    def add_task(self, title, start_date=None,
                 end_date=None, remind_dates=None, status=None, owned_by=None, subtasks=None, tags=None, can_edit=None):

        t = Task(title,self.current_user,start_date=start_date,end_date=end_date,remind_dates=remind_dates,status=status,owned_by=owned_by,subtasks=subtasks,tags=tags,can_edit=can_edit)
        self.tasks_manager.create_new_task(t)
        self.tasks_manager.save_to_DB()

    @log_decorator
    def remove_task(self, task_id):
        self.tasks_manager.remove_task(task_id)
        self.tasks_manager.save_to_DB()

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
        self.tasks_manager.edit_task(task_id, params_dict)
        self.tasks_manager.save_to_DB()

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
        reminders = self.tasks_manager.select_actual_reminders(date,delta)
        actual_tasks = self.tasks_manager.select_actual_tasks(date,delta)
        return (actual_tasks,reminders)

