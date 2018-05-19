from main_instances import Task
import datetime as dt
from Listener import BaseListener
from collections import OrderedDict

class TimeManager:
    def __init__(self,head_task, *listeners):
        self.head_task = head_task
        self.listeners = listeners
        self.today_dashboard = head_task
        self.next_5_minutes_tasks = None #dict() of 3 dicts with tasks{"start","continue","end"}

    def get_next_five_minutes(self):
        self.today_dashboard.sort_all_levels_by_priority()
        self.next_5_minutes_tasks = self.today_dashboard.select_next_5_minutes_tasks()
        self.next_5_minutes_tasks['start'] = OrderedDict(sorted(self.next_5_minutes_tasks['start'].items(),
                                                        key=lambda k, v: v.priority))
        self.next_5_minutes_tasks['continue'] = OrderedDict(sorted(self.next_5_minutes_tasks['continue'].items(),
                                                        key=lambda k, v: v.priority))
        self.next_5_minutes_tasks['end'] = OrderedDict(sorted(self.next_5_minutes_tasks['end'].items(),
                                                        key=lambda k, v: v.priority))
        return self.next_5_minutes_tasks


    def notify_listeners(self):
        for l in self.listeners:
            if l is issubclass(BaseListener):
                l.notify_me(self.next_5_minutes_tasks)
            else:
                raise TypeError("The "+type(l)+"is not a subclass of BaseListener")

