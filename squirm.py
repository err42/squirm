#!/usr/bin/env python3
import os
import sys
import logging
import threading
import schedule
import datetime
import time
import subprocess
from functools import partial
from pathlib import Path

## init globals
count = 0
pwd = Path.cwd()

## add logging
logging.basicConfig(
    level=logging.INFO,
    filename="squirm.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)

## execute jobs
def run_threaded(job_func):
    job_path = Path(job_func)
    print(
         "Starting",
         job_path,
         "running on thread %s" % threading.current_thread(),
     )
    job_thread = threading.Thread(target=job_path)
#    job_thread = threading.Thread(target=job_func)
####    job_thread = subprocess.run(['python3', job_path])
    start_time = time.time()
#    job_thread.start()
#    job_thread.join()  # Wait for the thread to finish
    end_time = time.time()
    diffr = end_time - start_time
    logging.info("run_threaded ran in %s seconds" % diffr)
    print(diffr)

def run_regular(dep_func):
    tmp_path = str(pwd) + "/" + str(dep_func)
    dep_path = Path(tmp_path)
    print(
         "Starting",
         dep_path,
         "running on thread %s" % threading.current_thread(),
     )
    start_time = time.time()
    process = subprocess.Popen(dep_path, shell=False, stdout=subprocess.PIPE)
    end_time = time.time()
    diffr = end_time - start_time
    process.wait()
    logging.info("run_regular ran in %s seconds" % diffr)
    print(diffr)

## confirm file exists and is pythonic
def validate_job(job):
    global count
    count += 1
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
    global count
    inputfile = sys.argv[1]
    wall_time = '-'
    with open(inputfile, "r") as task_list:
        for lines in task_list.read().splitlines():
            curr_line = lines.split()
            name = str(curr_line[0])
            time_est = curr_line[1]
            job_req = str(curr_line[2:])
            ## throws exception if commit flag not thrown when checked, so caught & ignored.
            try:
                committed = str(sys.argv[2])
            except IndexError:
                committed = 0
                pass

            ## remove formatting from dep list
            strippedvals = (
                job_req.replace("[", "")
                .replace("]", "")
                .replace("'", "")
                .replace(",", "")
            )

            ## validate tasks, consider depends
            retval = validate_job(name)
            if retval == 0:
                isvalid = "YES"
                if str(job_req) == "[]":
                    job_req = None
                print(
                     "Order",
                     count,
                     "Task Name:",
                     name,
                     "Is Valid?",
                     isvalid,
                     "Est.Time",
                     time_est,
                     "Wall.Time",
                     wall_time,
                     "Dependencies",
                     str(job_req),
                 )
                ## run if no job depends
                if committed != 0:
                     print(
                          "--commit flag caught & task validated. Now running independent (parallel) task",
                          name,
                          ":",
                      )
                     run_threaded(name)

                    
                if job_req is not None:
                    if committed != 0:
                        ## run primary task outside of dep loop
                        print(
                             "--commit flag caught & task(s) validated. Now running dependent tasks",
                             name,
                             ":",
                         )
                        run_regular(name)

                    ## check deps validity
                    for dep in strippedvals.split():
                        depval = validate_job(dep)
                        if depval != 0:
                            isvalid = "DEP. FAIL"
                            print(
                                "Order",
                                count,
                                "Task dependency",
                                dep,
                                "NOT VALID and therefore will not be submitted. Received Return Code:",
                                depval,
                            )
                        else:
                            isvalid = "YES"
                            if committed != 0:
                                print(
                                     "--commit flag caught & task(s) validated. Now running dependent tasks",
                                     dep.split(),
                                     ":",
                                 )
                                run_regular(dep)


                               
                            else:
                                print(
                                    "Order",
                                    count,
                                    "Dependency Name:",
                                    dep,
                                    "Is Valid?",
                                    isvalid,
                                    "Est.Time",
                                    time_est,
                                    "Wall.Time",
                                    wall_time,
                                )
#                else:
#                    isvalid = "YES"
#                    count += 1
#                    print(
#                        "Order",
#                        count,
#                        "Task Name:",
#                        name,
#                        "Is Valid?",
#                        isvalid,
#                        "Est.Time",
#                        time_est,
#                        "Wall.Time",
#                        wall_time,
#                        "Dependencies",
#                        str(job_req),
#                    )



            else:
                isvalid = "PRI.FAIL"
                count += 1
                print(
                    "Order",
                    count,
                    "Task Name:",
                    name,
                    "Is Valid?",
                    isvalid,
                    "Est.Time",
                    time_est,
                    "Wall.Time",
                    wall_time,
                    "Dependencies",
                    str(job_req),
                )

#    schedule.run_pending()


if __name__ == "__main__":
    main()
