

class PlansManager:
    def __init__(self, plans_dict=None):
        if plans_dict is None:
            self.plans = {}
        else:
            self.plans = plans_dict

    def add_plan(self, plan):
        self.plans[plan.uid] = plan

    def remove_plan(self,plan_id):
        self.plans.pop(plan_id)

    def try_find_plan_for_task(self, task_id):
        for k,v in self.plans.items():
            if v.task_id == task_id:
                return k
        return None

    def get_updates(self):
        tasks_to_add = []
        for k,v in self.plans.items():
            while v.periodic_update_needed():
                tasks_to_add.append(v.get_next_periodic_task())
        return tasks_to_add
