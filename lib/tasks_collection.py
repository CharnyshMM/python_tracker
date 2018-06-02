from lib.task import *

class TasksCollection:
    def __init__(self, db_answer=None):
        #get_all_tasks_to, now it is a dict with id_s as keys
        if db_answer is None:
            self.tasks = dict()
        else:
            self.tasks = db_answer

    def add_task(self,new_task):
        self.tasks[new_task.get_attribute(TaskAttributes.UID)] = new_task

    def find_and_add_to_attribute(self,id_to_find,attr,value,user):
        task_node = self.tasks[id_to_find]
        task_node.add_to_attribute(attr,value,user)

    def find_and_set_attribute(self,id_to_find,attr,value,user):
        task_node = self.tasks[id_to_find]
        task_node.set_attribute(attr,value,user)

    def find_and_remove_from_attribute(self,id_to_find, attr, value,user):
        task_node = self.tasks[id_to_find]
        task_node.remove_from_attribute(attr,value,user)

    def find_and_unset_attribute(self,id_to_find,attr,user):
        task_node = self.tasks[id_to_find]
        task_node.unset_attribute(attr,user)

    def find_task(self,id_to_find):
        return self.tasks[id_to_find]

    def get_all_tasks(self):
        return list(self.tasks.values())

    def select_tasks_by_key(self, key):
        result_dict = dict()
        for k,v in self.tasks.items():
            if key(v):
                result_dict[k] = v

        return TasksCollection(result_dict)

    def remove_task_by_id(self,id):
        self.tasks.pop(id)







