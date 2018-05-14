import main_instances as mi
import datetime as dt



class TimeManager:
    def __init(self,head_task):
        self.head_task = mi.Task(head_task)
        self.ordered_tasks_queue = list()
        self.today_dashboard = mi.Task.from_dict(self.head_task.select_subtasks(key=TimeManager.is_today_task),head_task.ownder)
        self.next_5_minutes_tasks = None #dict() of 3 dicts with tasks{"start","continue","end"}

    def get_next_five_minutes(self):
        self.today_dashboard.sort_all_levels_by_priority()
        self.next_5_minutes_tasks = self.today_dashboard.select_next_5_minutes_tasks()
        return self.next_5_minutes_tasks



