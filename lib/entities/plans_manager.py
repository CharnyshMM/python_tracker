"""This module contains a PlansManager class"""


class PlansManager:
    """Simple class that stores plans and collects updates from them"""

    def __init__(self, plans_dict=None):
        if plans_dict is None:
            self.plans = {}
        else:
            self.plans = plans_dict

    def add_plan(self, plan):
        self.plans[plan.uid] = plan

    def remove_plan(self,plan_id):
        self.plans.pop(plan_id)

    def find_plans_for_task(self, task_id):
        """
        Find a plan by task id of connected task. If not found returns None
        task_id:
        """
        results = []
        for k,v in self.plans.items():
            if v.task_id == task_id:
                results.append(v)
        return results

    def get_updates(self):
        """Checks each plan if it needs update and if True, collects a new task from it.
        returns a list of new tasks created by plans
        """
        tasks_to_add = []
        for k,v in self.plans.items():
            while v.periodic_update_needed():
                tasks_to_add.append(v.get_next_periodic_task())
        return tasks_to_add
