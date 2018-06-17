# Py_Tracker
 a tiny python application for managing tasks and plans

## Py_Tracker's basic functionality:

 - creating, editing, storing & removing a single task record
 - organising hierarchy of tasks and subtasks
 - single task attributes include start time, end time, multiple reminders, tags
 - users & command working: each task has an Author and the Author can add or remove people who can make changes to this task. Other users are able just to read info of this task
 - periodic plans. They can create a new task record according to a template each time the specified period ends. And this newborn task has everything its template task has but time values of start, end and reminders are moved period forward
 - console interface: `$ py_tracker <object> <action> [arguments] ` format

Py_Tracker package includes a library that can be used separately from console interface. You can just import it
in your Python3 interpreter and use its task_interface module just like a non-console UI version or you can use
the classes provided in library to create your own cool projects.

## Installing
Clone the repo and install the setup.py. Python 3 required.
    
    git clone https://charnysh@bitbucket.org/charnysh/python_tracker.git
    
Navigate to the directory, containing the files you've downloaded adn run this:

    $ python3 setup.py install
    
To run unittests included in library run:

    $ python3 setup.py test


## Getting started with console interface:

### First steps
Type py_tracker in console:

    $ py_tracker 

The program will ask you to enter your user_name. It's just for the first time. Program remembers the last user username.
So, to start working, type:

    $ py_tracker user set 'your_name'

You are in! Now let's add a new task. Type the following:

    $ py_tracker task add 'My first task' 

If the process was succesful you'll see a message right after the command:

`"Task created. Its id is '.....-.....-.....-.....'".` 

The `'.....-.....-.....-.....'` would be some string of digits & letters. It's an id of the newborn task.

You have no need to remember tasks ids. It's always possible to find the task by name or other attributes with the task find command:

     $ py_tracker task find 'My first task' 

Or you can just call task print command to see all the tasks:

    $ py_tracker task print 
   
You can print one task by specifying its id to the task print command:

    $ py_tracker task print -id '.....-....-.....-.....'
  
There are much more task options that can be set at the time of creating a task. For example, let us create another task
that has a start date:

    $ py_tracker task add 'My second task' --starts '12/6/2018 13:23'  

Note that the date format 'dd/mm/yy hh:mm' is the only format the program understands. It'll notify you if your
date was not recognised. And if you want to quickly set some time attribute with the current time & date you can
just type `now`:

    $ py_tracker task add 'Right now task' --starts now
    
And, finally, if you don't specify a date, the program will treat the task as having no time limits.


To see all the options a command has feel free to ask for **help** with `-h` or `--help`

### Task attributes editing and using

The task id is needed when you want to make changes to a particular task. Let's set a start date attribute.
(if you will try to read help manual with -h or --help after each command we use here you'll see that all
the task attributes can be set at a step of creating task and not all the attributes can be edited afterwards).
Instead of `'.....-.....-.....-.....'` put id of task you'd like to make changes to. 

    $ py_tracker task edit '.....-.....-.....-.....' set --status complete 
    
Every task can have multiple (or none) tags. Tags can be used to unite completely different tasks. Tag is just a user 
defined string. And since task can have multiple tags `edit add` and `edit rm` commands are used to set and unset 
such attributes.

    $ py_tracker task edit '.....-.....-.....-.....' add --tag buy_when_shopping
    
You can use find command to list tasks with required tags. The command below searches for tasks with tasks _Camping_, _Summer_

    $ py_tracker task find --tags Camping Summer
    
There are also Reminders. Every task can have multiple reminders set. They are just a time records that tell program
when to notify you about them. They can be set on a step of creating a new task or added later:

    $ py_tracker task edit '.....-.....-.....-.....' add --reminder '14/6/18 23:23'

### Tasks hierarchy

Py_Tracker can help you with organising tasks hierarchy. You can add subtasks to existing tasks. This is specified 
at a time of creating a new task with `task add` command. Look at the example (`'.....-.....-.....-.....'` is parent task id):

    $ py_tracker task add 'Sub Task Name' --parent '.....-.....-.....-.....' .
    
You can also specify all the attributes the task can have. The only limitation there exists is that your subtasks can't end 
later than their parent task.

### Removing a task

Removing a task is also simple. Just get the id of task you want to delete and run:

    $ py_tracker task rm '.....-.....-.....-.....'
    
By default Py_Tracker checks if the task you want to remove has subtasks. And if it has program will abort
deleting and warn you about that. But there is an `-f` option for `rm` command. It forses the program to 
delete the task and to remove all the subtasks.

### Checking actuals

All the dates that can be set in program are more than just some labels. The `check` command is used to collect all updates,
all starting, ending and continuing tasks, all reminders that are actual currently (+/- 5 minutes) and print a structured 
report.

    $ py_tracker check
    
### Periodic Plans

You can set periodical repetitions for existing tasks. If you set one the program will track it and when the time period
you've set runs out it will automatically create a new task that has the same attributes the previous task has but all the 
times and dates are moved forward exactly on a period.
Imagine you have already created a task with id '.....-.....-.....-.....'. Now let's set a plan to repeat the task every 3 hours and stop repeating
in '14/6/18 23:39'
So we need to add a plan:

    $ py_tracker plan add '.....-.....-.....-.....' --hours 3 --finish '14/6/18 23:39'
    
And each time we run `check` command the program will check if this plan needs updates and if yes it will create a new task.
You can add plans without setting finish time (it will never stop) or select another period. There are fixed periods: 
`--fixed yearly` or `--fixed monthly` or `--fixed daily`. Or more adjustable ones `--days N`, `--hours N`, `--mins N` where N is the number 
you type in.

Plans also have ids and also have their own print command

    $ py_tracker plan print
    
Or you can get a plan id from a task that was created automatically by plan. You should run `task print` command with wide `-w` option.

To unset a plan simply remove it. No tasks would be hurt. (`'.....-.....-.....-.....'`  is **Plan** id)

    $ py_trakcer plan rm '.....-.....-.....-.....' 

