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


TASK LIST EXAMPLE CONTENTS:
first.py 10
second.py 20 third.py 
fourth.py 30 fifth.py sixth.py


LOG (INFO) SAMPLE OUTPUT:

07:35:55 INFO first.py ran in 2.384185791015625e-07 seconds so difference in time was 9.999999761581421 seconds
07:36:00 INFO second.py ran in 5.037276029586792 seconds so difference in time was 14.962723970413208 seconds
07:36:05 INFO third.py ran in 5.009338140487671 seconds so difference in time was 14.990661859512329 seconds
07:36:10 INFO fourth.py ran in 5.01104736328125 seconds so difference in time was 24.98895263671875 seconds
07:36:16 INFO fifth.py ran in 5.009309768676758 seconds so difference in time was 24.990690231323242 seconds
07:36:21 INFO sixth.py ran in 5.010116815567017 seconds so difference in time was 24.989883184432983 seconds


COMMAND LINE SAMPLE OUTPUT:

Order 1 Task Name: first.py Is Valid? YES Est.Time 10 Wall.Time - Dependencies []
--commit flag caught & task validated. Now running independent (parallel) task first.py :
Starting first.py running on thread <_MainThread(MainThread, started 139927336523584)>
first.py ran in 2.384185791015625e-07 seconds so difference in time was 9.999999761581421 seconds
Order 2 Task Name: second.py Is Valid? YES Est.Time 20 Wall.Time - Dependencies ['third.py']
--commit flag caught & task(s) validated. Now running dependent tasks second.py :
Starting /home/err/bin/PYTHON/FOR_EMPLOYER/squirm/second.py running on thread <_MainThread(MainThread, started 139927336523584)>
second.py ran in 5.037276029586792 seconds so difference in time was 14.962723970413208 seconds
--commit flag caught & task(s) validated. Now running dependent tasks ['third.py'] :
Starting /home/err/bin/PYTHON/FOR_EMPLOYER/squirm/third.py running on thread <_MainThread(MainThread, started 139927336523584)>
third.py ran in 5.009338140487671 seconds so difference in time was 14.990661859512329 seconds
Order 4 Task Name: fourth.py Is Valid? YES Est.Time 30 Wall.Time - Dependencies ['fifth.py', 'sixth.py']
--commit flag caught & task(s) validated. Now running dependent tasks fourth.py :
Starting /home/err/bin/PYTHON/FOR_EMPLOYER/squirm/fourth.py running on thread <_MainThread(MainThread, started 139927336523584)>
fourth.py ran in 5.01104736328125 seconds so difference in time was 24.98895263671875 seconds
--commit flag caught & task(s) validated. Now running dependent tasks ['fifth.py'] :
Starting /home/err/bin/PYTHON/FOR_EMPLOYER/squirm/fifth.py running on thread <_MainThread(MainThread, started 139927336523584)>
fifth.py ran in 5.009309768676758 seconds so difference in time was 24.990690231323242 seconds
--commit flag caught & task(s) validated. Now running dependent tasks ['sixth.py'] :
Starting /home/err/bin/PYTHON/FOR_EMPLOYER/squirm/sixth.py running on thread <_MainThread(MainThread, started 139927336523584)>
sixth.py ran in 5.010116815567017 seconds so difference in time was 24.989883184432983 seconds 
