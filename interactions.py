import main_instances
import datetime

class path:
    def __init__(self,current):
        self.path = []
        self.path.append(current)

    def append(self,next):
        self.path.append(next)

    #организовать определение и построение пути к задаче

class SessionManager:
    def __init__(self, user):
        #retrieve users_dashboard from DB
        self.dashboard = self.initialise(self)

    @staticmethod
    def initialise():
        """
        perfors start of TM
        :return: dashboard with whole hierarchy of tasks
        """
        print("loading data from database...")
        dashboard = main_instances.DBManager.do_loarding()
        task1 = main_instances.Task("wash the dishes",dashboard.author,dashboard)
        task1.due_date = datetime.datetime(2018,4,17,0,0)
        task1.priority = 4
        dashboard.subtasks.add_task(task1)
        task2 = main_instances.Task("play the game", dashboard.author, dashboard)
        task2.due_date = datetime.datetime(2018, 4, 16, 20, 0)
        task2.priority = 7
        dashboard.subtasks.add_task(task2)
        return  dashboard

    def print_dashboard(self):
        for each in self.dashboard.subtasks:
            each.to_line(0);

    def add_task(self):
        print("TASK CREATION:")
        message = input("Task message:")


    def path_finder(self,path):
