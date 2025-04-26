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
    print("Starting", {j}, "running on thread %s" % threading.current_thread())


## confirm file exists and is pythonic
def validate_job(*jb):
    try:
        result = subprocess.run(
            ["black", "--check", "-q", str(jb), "2>/dev/null"],
            capture_output=True,
            shell=True,
            text=True,
        )
        return result
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
            for curr_word in curr_line:
                name = str(curr_line[0])
                time_est = str(curr_line[1])
                job_req = str(curr_line[2:])
                print(
                    "Name:", name, "Est. Time", time_est, "Dependencies", str(job_req)
                )
                ## reorganize jobs based on dependencies

                ## run jobs if user committed
                retval = validate_job(name)
                schedule.every(1).seconds.do(announce_job)
                try:
                    committed = str(sys.argv[2])
                except IndexError:
                    committed = 0
                    pass
                if committed == "--commit":
                    if retval != 0:
                        count += 1
                        schedule.every(1).seconds.do(announce_job, run_threaded)
                    while True:
                        schedule.run_pending()
                        time.sleep(1)


if __name__ == "__main__":
    main()
