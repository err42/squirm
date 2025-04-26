import sys
import threading
import schedule
import time
import subprocess

## execute jobs
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

## increase verbosity
def announce_job(j):
    print("Starting", {j}, {counter}, "running on thread %s" % threading.current_thread())

## confirm file exists and is pythonic
def validate_job(*jb):
    try:
        subprocess.check_output(['black', '--check', '-q', jb, '2>/dev/null'], shell=True)
    except subprocess.CalledProcessError as blkexc:
        return blkexc.returncode

## get jobs from user
def main():
    count = 0
    inputfile = sys.argv[1]
    with open(inputfile, 'r') as task_list:
        for lines in task_list.read().split("\n")[::2]:
#           lines = task_list.read().splitlines()
            for curr_line in lines:
               count += 1
               name = curr_line[0]
               time_est = curr_line[1]
               job_req = curr_line[2:]
               print("Name:", name, "Est. Time", time_est, "Dependencies",  job_req)
#           print(name)
#           print(time_est)
#           print(job_req)
## reorganize jobs based on dependencies
## run jobs if user committed
        retval = validate_job(task)
        if sys.argv[2] == "--commit"
            if retval == 0:
                counter += 1
                schedule.every(1).seconds.do(announce_job, run_threaded)
                while True:
                    schedule.run_pending()
                    time.sleep(1)

if __name__ == "__main__":
    main()
