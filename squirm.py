import sys
import threading
import schedule
import time
import subprocess
from functools import partial


## execute jobs
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    start = datetime.datetime.now()
    job_thread.start()
    job_thread.join()
    end = datetime.datetime.now()
    return end - start


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
        for lines in task_list.read().splitlines():
            curr_line = lines.split()
            name = str(curr_line[0])
            time_est = curr_line[1]
            job_req = str(curr_line[2:])
            wall_time = "-"
            count += 1
            ## throws exception if no deps given, so ignored.
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
                if job_req is not None:
                    ## check deps validity
                    for dep in strippedvals.split():
                        depval = validate_job(dep)
                        if depval != 0:
                            print(
                                "Task",
                                dep,
                                "NOT VALID and therefore will not be submitted. Received Return Code:",
                                depval,
                            )
                            isvalid = "DEP. FAIL"
                            break
                        else:
                            isvalid = "PASS"
                else:
                    isvalid = "PASS"
                    print(
                        "Order",
                        count,
                        "Task Name:",
                        name,
                        "Is Valid?",
                        isvalid,
                        "Est. Time",
                        time_est,
                        "Wall Time",
                        wall_time,
                        "Dependencies",
                        str(job_req),
                    )

                    ## run jobs if user committed
                    if committed != 0:
                        print(
                            "--commit flag caught & task(s) validated. Now running #",
                            count,
                            ":",
                        )
                        print(
                            "Starting",
                            name,
                            "running on thread %s" % threading.current_thread(),
                        )
                        schedule.every(1).seconds.do(partial(run_threaded, name))
                        print(
                            "Order",
                            count,
                            "Task Name:",
                            name,
                            "Is Valid?",
                            isvalid,
                            "Est. Time",
                            time_est,
                            "Wall Time",
                            wall_time,
                            "Dependencies",
                            str(job_req),
                        )

            else:
                isvalid = "PRI. FAIL"
                print(
                    "Order",
                    count,
                    "Task Name:",
                    name,
                    "Is Valid?",
                    isvalid,
                    "Est. Time",
                    time_est,
                    "Wall Time",
                    wall_time,
                    "Dependencies",
                    str(job_req),
                )

    schedule.run_pending()


if __name__ == "__main__":
    main()
