# Squirm 0.0.001
basic task scheduler built initially on Python 3.11.2

Usage:
    squirm.py [options] ... [ --task-name <optional_task_name> | --run-task <task_name> | --when-to-run  | --depends-on <task_name> | --commit ] ...

    NOTE: Squirm always defaults to 'dry run' and produces a report of tasks collected and their validation status (should it run?). 
          You MUST pass the '--commit' flag in order to make changes to the system.

    NOTE: Squirm assumes order to be FIFO but does proiritize dependencies over otherwise scheduled tasks.


EXAMPLES:
INPUT


                squirm --run-task /home/testuser/solo_task.py
                

(dry-run)       squirm --task-name "first_task" --run-task "first_task.py" 


                squirm --task-name "primary_task" --run-task "secondary_task.py" --depends-on "first_task" --commit


                squirm --task-name "final_task" --run-task "last_task.py" --depends-on "another_task" --commit



OUTPUT

        SQUIRM SCHEDULED TASKS VALIDATION:

            ORDER.#.NAME    TASK     DEPENDS.ON       VALID?      EXP.TIME    WALL.TIME   DIFF
                1         first.py       -              YES         .13          .30      .17
                2        second.py     first.py         YES         .11          .27      .16
                3         third.py    second.py         YES         .10          .26      .15
                4        final_task   another_task       NO           -           -         - 
 
