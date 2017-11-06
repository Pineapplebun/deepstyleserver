import Queue, sqlite3, logging, os, sys
from subprocess import Popen

"""
A job that contains information about the POST request.
Required information:
path to file
content weight
style weight
etc...

gpu: int
"""
class job(object):
    def __init__(self, entry_id, absolute_path_to_image1, absolute_path_to_image2, output_path, content_weight, style_weight):
        self.job_id = entry_id
        self.path1 = absolute_path_to_image1
        self.path2 = absolute_path_to_image2
        self.out = output_path
        self.content_weight = content_weight
        self.style_weight = style_weight
        self.gpu = None
        self.proc = None
        self.finished = None

    def __str__(self):
        return "%s : %s : %s" % (self.path1, self.path2, self.out)

class logger(object):
    """
    Create a logger and write to console and file.
    """
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler("js_logger.txt")

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        self.ch.setFormatter(formatter)
        self.fh.setFormatter(formatter)

    def shutdown(self):
        logging.shutdown()

"""
Job scheduler queries a POST REQUEST from the database and creates a job sent to
the queue. If the job is first in the queue and there is gpu space, by checking a list of
current processes, then we execute the job in shell and place the job in CURRENT_RUNNING.
When the job is finished running, it will be removed from the CURRENT_RUNNING
list. The data from the job will be recorded.
"""
class job_scheduler(object):
    def __init__(self, num_gpus, name_db):
        self.logger = logger()
        self.num_gpus = num_gpus
        self.gpu_free = Queue.Queue()
        self.running_jobs = []
        self.job_queue = Queue.Queue()
        self.db = sqlite3.connect(name_db)
        # Assuming that the gpu ranges from 0 to num_gpus - 1
        # gpu_0, gpu_1, etc.
        for i in range(num_gpus):
            gpu_free.put(i)

    def create_jobs_and_queue(self):
        """
        Retrieve the unqueued jobs, create job objects and queue them
        to the job_queue. Modify the job as 'queued' in the database.
        """
        c = self.db.cursor()
        new_job_exists = False
        for row in c.execute("SELECT * FROM jobs WHERE status='unqueued'"):
            job_queue.put(job(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
            # Set queue status of current row's id to be 'queued'
            c.execute("UPDATE jobs set status = 'queued' WHERE rowid = %s" % (row[0],))
            new_job_exists = True
        c.close()
        if new_job_exists:
            self.db.commit()

    def assign_gpu_and_run(self):
        """
        Add a job to the currently running list and remove from the job queue.

        Remove from the gpu_free queue and set the environmental variable
        CUDA_VISIBLE_DEVICES to be the gpu number. This is important because
        we do not want tensorflow to allocate memory from other gpus since it
        impedes the ability to run another process on a different gpu.

        NOTE: NEED TO CHANGE THE TENSORFLOW EVALUATE SCRIPT TO ALLOW
        SOFT PLACEMENT IN THE SESSION.
        """
        if not gpu_free.is_empty():
            job_to_run = job_queue.get()
            job_to_run.gpu = gpu_free.get()

            # Create a copy of the environemnt
            new_env = os.environ.copy()
            new_env['CUDA_VISIBLE_DEVICES'] = str(job_to_run.gpu)
            # Run the subprocess
            job_to_run.proc = Popen(['python', 'neural_style.py', '--content',
            '%s' % job_to_run.path1, '--styles', <style file>, '--output',
            '%s' % job_to_run.path], env=new_env)

            # Append the job to the running_job list
            running_procs.append(job_to_run)

    def main():
        """
        Create a pool of processes equivalent to the number of gpus
        Need async multiprocessing here...
        """
        while True:
            # When a new job exists in the database, create a job and load
            # into the job queue.
            self.create_jobs_and_queue()

            # When a job exists in the job queue
            if not job_queue.is_empty():
                while not gpu_free.is_empty():
                    self.assign_gpu_and_run()

            # Check the processes that are running
            # If proccesses are still running then this loop will continue to
            # run until a process is finished. Once a process has finished,
            # we can check if any requests are made and then create jobs from
            # them and we can check if any jobs are waiting. GPU bound.
            completed_job = None
            for job_i in running_jobs:
                exit_code = job_i.proc.poll()
                if exit_code is not None:
                    completed_job = running_procs.remove(job_i)
                    gpu_free.put(completed_job.gpu)
                    self.logger.info(job_i)
                    break

            if exit_code != 0 and completed_job is not None:
                self.logger.error(job_i)


if __name__ == '__main__':
    js = job_scheduler(num_gpus =sys.argv[1], name_db=sys.argv[2])
    js.main()
