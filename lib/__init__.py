r"""Py_Tracker lib is an instrument for simple task and plan management.
It can be used alone from your Python interpreter or you can cover it with custom UI.

USAGE EXAMPLES--------------------------------------------------------------------

    1. Create a task and add it

    >>> from lib.entities.task import Task, TaskAttributes, TaskPriority, TaskStatus
    >>> from lib.interface import Interface
    >>> from lib.json_db.interface import DB
    >>> import datetime as dt
    >>> interface = Interface(db_adapter=DB(), user='username')
    >>> task = Task(title='My new task', author='usrname', status=TaskStatus.ACTIVE, start_time=dt.datetime.now())
    >>> interface.add_task(task)

    2. Create a subtask for existing task and add it to storage (all the imports from the the previous example)
    >>> task = Task(title='Parent task', author='username')
    >>> interface = Interface(db_adapter=DB(), user='username')
    >>> interface.add_task(task)
    >>> parent_id = task.get_attribute(TaskAttributes.UID)
    >>> subtask = Task(title='Subtask', author='username', parent=parent_id)
    >>> interface.add_task(subtask) # program automatically adds a subtask record to a parent task that is already stored

    3. Remove a task:
    >>> interface.remove_task(task.get_attribute(TaskAttributes.UID))
    # if the task has subtasks this method will raise SubtasksNotRemovedError.
    >>> interface.remove_with_subtasks(task.get_attribute(TaskAttributes.UID))

    4. Modify task:
    >>> interface.task_set_attribute(task_id=task.get_attribute(TaskAttributes.UID),
    ...                              attribute=TaskAttributes.TITLE,
    ...                              value='New title')

    5. Create a periodic plan:
    >>> task = interface.get_task(task_id)
    >>> user = task.get_attribute(TaskAttribute.AUTHOR)
    >>> interface.add_periodic_plan(period=Period.DAILY, task_template=task, task_id=task_id)

    6. Check actuals:
    >>>actual_tasks, reminders = interface.check_time()
    actual_tasks['starting'] # dict of  tasks that start currently
    actual_tasks['ending'] # dict of tasks that are ending soon
    actual_tasks['continuing'] # dict of tasks started earlier and aren't ending soon

    reminders # dict of tasks that have reminders set on current time.



"""
