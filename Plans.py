from enum import IntEnum
import datetime as dt

class PlanType(IntEnum):
    EVERY_DAY = 1
    EVERY_WEEK = 2
    EVERY_MONTH = 3
    EVERY_YEAR = 4
    EVERY_TIMEDELTA = 5
    CONDITIONAL = 6

# class Plan:
#
#     @staticmethod
#     def create_periodic_plan(task_template, timedelta, start_time=None, end_time=None):
#         plan = Plan()
#         plan.type = PlanType.PERIODIC
#         plan.timedelta = timedelta
#         plan.task_template = task_template
#         if start_time is None:
#             start_time = dt.datetime.now()
#         plan.start_time = start_time
#         plan.end_time = end_time
#         plan.check_condition = Plan.check_time
#
#         return plan



    # @staticmethod
    # def create_conditional_plan(task_template,condition_checker,end_condition=None):
    #     plan = Plan()
    #     plan.type = PlanType.CONDITIONAL
    #     plan.


    # @classmethod
    # def check_time(self):
    #     now = dt.datetime.now()
    #     if self.