import threading
import time
import schedule
import datetime
import concurrent.futures

counter = 0

def run_job(j):
    counter += 1
    print("Starting {_j} {_counter} running on thread %s" % threading.current_thread())
    # run concurrent job

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

## get args from user
## validate jobs
## run jobs based on dependencies

def validate_job(jb):
    try:
        result = subprocess.check_output(['black', '--check', '-q', str(_jb), '2>/dev/null'], shell=True, check=True)
    except subprocess.CalledProcessError as blkexc:                                                                                                   
        return blkexc.returncode

while 1:
    current_time = datetime.datetime.now().time()
    schedule.run_pending()
    schedule.every(1).seconds.do(run_threaded, job)
