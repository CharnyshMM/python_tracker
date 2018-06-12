# Py_Tracker
 a tiny python application for managing tasks and plans

### Py_Tracker's basic functionality:
 - creating, editing, storing & removing a single task record
 - organising hierarchy of tasks and subtasks
 - single task attributes include start time, end time, multiple reminders, tags
 - users & command working: each task has an Author and the Author can add or remove people who can make changes to this task. Other users are able just to read info of this task
 - periodic plans. They can create a new task record according to a template each time the specified period ends. And this newborn task has everything its template task has but time values of start, end and reminders are moved period forward
 - console interface: `$ py_tracker <object> <action> [arguments] ` format

Py_Tracker package includes a library that can be used separately from console interface. You can just import it
in your Python3 interpreter and use its task_interface module just like a non-console UI version or you can use
the classes provided in library to create your own cool projects.

### Installing
Clone the repo and install the setup.py. Python 3 required.

$ how to clone & install

## Getting started with console interface:

Type py_tracker in console:

` $ py_tracker `

The program will ask you to enter your user_name. It's just for the first time. Program remembers the last user username.
So, to start working, type:

` $ py_tracker user set 'your_name' `

You are in! Now let's add a new task. Type the following:

` $ py_tracker task add 'My first task' `

If the process was succesful you'll see a message right after the command:

"Task created. Its id is 'f849390-.....'"  - some long code. This is a task id. You have no need to remember it.
It's always possible to find the task by name or other attributes with the task find command:

` $ py_tracker task find 'My first task' `

Or you can just call task print command to see all the tasks:

` $ py_tracker task print `

The task id is needed when you want to make changes to a particular task. Let's set a start date attribute.
(if you will try to read help manual with -h or --help after each command we use here you'll see that all
the task attributes can be set at a step of creating task and not all the attributes can be edited afterwards).

` $ py_tracker task edit 'f84939-0....-.....-.....' set -starts '12/6/2018 13:23' `

Note that the dateformat 'dd/mm/yy hh:mm' is the only format the program understands. It'll notify you if your
date was not recognised. And if you want to quickly set some time attribute with the current time & date you can
just type now:

    $ py_tracker task edit 'f84939-0....-.....-.....' set -starts now


You can print one task by specifying its id to the task print command:

    $ py_tracker task edit 'f84939-0....-.....-.....' set -starts now

