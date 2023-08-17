import time
from rq import get_current_job

def background_task(n):
    ## for 1 to 100 update the meta value
    job = get_current_job()
    print(job)
    for i in range(100):
        job.meta['progress'] = i
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print("Task completed!")
    return n + 1
    
