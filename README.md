# Squirm 0.0.001
basic task scheduler built initially on Python 3.11.2

Usage:
    squirm.py [ <task_list.txt> [--commit] ]

    NOTE: Squirm always defaults to 'dry run' and produces a report of tasks collected and their validation status (should it run?). 
          You MUST pass the '--commit' flag in order to make changes to the system.

    NOTE: Squirm assumes order to be FIFO but does handle priorities in dependencies.


EXAMPLES:
INPUT


(dry-run)       squirm task_list.txt

                squirm task_list.txt --commit

OUTPUT

        SQUIRM SCHEDULED TASKS VALIDATION:

            ORDER.#.NAME    TASK     DEPENDS.ON       VALID?      EXP.TIME    WALL.TIME   DIFF
                1         first.py       -              YES         .13          .30      .17
                2        second.py     first.py         YES         .11          .27      .16
                3         third.py    second.py         YES         .10          .26      .15
                4        final_task   another_task       NO           -           -         - 
 
