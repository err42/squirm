import sys
import threading
import schedule
import time
import subprocess
from pathlib import Path

## execute jobs
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


## confirm file exists and is pythonic
def validate_job(job):
    try:
        result = subprocess.run(
            ["black", "--check", "-q", job],
            capture_output=True,
            text=True,
        )
        return result.returncode
    except subprocess.CalledProcessError as blkexc:
        return blkexc.returncode


## get jobs from user
def main():
    count = 0
    inputfile = sys.argv[1]
    with open(inputfile, "r") as task_list:
        # for lines in task_list.read().split("\n")[::2]:
        for lines in task_list.read().splitlines():
            curr_line = lines.split()
            name = str(curr_line[0])
            time_est = str(curr_line[1])
            job_req = str(curr_line[2:])
            wall_clock = 0
            count += 1
            retval = validate_job(name)
#            schedule.every(1).seconds.do(announce_job(name))
#           ## reorganize jobs based on dependencies
            try:
               committed = str(sys.argv[2])
            except IndexError:
                committed = 0
                pass
            ## run jobs if user committed
            if committed == "--commit":
                if retval == 0:
                   print("--commit flag caught, I would run this validated task list, as listed:")
                   schedule.every(1).seconds.do(run_threaded(name))
                   print("Starting", {j}, "running on thread %s" % threading.current_thread())
                   wall_time = '-' 
                   print( "Order", count, "Task Name:", name, "Est. Time", time_est, "Wall Time", wall_time, "Dependencies", str(job_req))
                elif retval != 0:
                    print("Task", name, "NOT VALID and therefore will not be submitted. Received Return Code:", retval)
            else:
                print("DRY RUN")
                wall_time = '-' 
                if retval == 0:
                    print("TASK IS VALID:")
                    print( "Order", count, "Task Name:", name, "Est. Time", time_est, "Wall Time", wall_time, "Dependencies", str(job_req))
                elif retval != 0:
                    print("TASK IS NOT VALID:")
                    print( "Order", count, "Task Name:", name, "Est. Time", time_est, "Wall Time", wall_time, "Dependencies", str(job_req))
#            while True:
#                schedule.run_pending()
#                time.sleep(1)


if __name__ == "__main__":
    main()
