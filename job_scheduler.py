import Queue, time
from subprocess import Popen

"""
A job that contains information about the POST request.
Required information:
path to file
content weight
style weight
etc...
"""
class job(object):
    def __init__(absolute_path_to_image1, absolute_path_to_image2, output_path, content_weight, style_weight):
        self.path1 = absolute_path_to_image1
        self.path2 = absolute_path_to_image2
        self.out = output_path
        self.content_weight = content_weight
        self.style_weight = style_weight
        self.gpu = None
        self.proc = None
        self.created = time.asctime(time.localtime(time.time()))
        self.finished = None


"""
Job scheduler queries a POST REQUEST from the database and creates a job sent to
the queue. If the job is first in the queue and there is gpu space, by checking a list of
current processes, then we execute the job in shell and place the job in CURRENT_RUNNING.
When the job is finished running, it will be removed from the CURRENT_RUNNING
list. The data from the job will be recorded.
"""
class job_scheduler(object):
    def __init__(self, num_gpus):
        self.num_gpus = num_gpus
        self.gpu_free = Queue.Queue()
        self.running_jobs = []
        self.job_queue = Queue.Queue()

    def assign_gpu_and_run(self):
        """
        Add a job to the currently running list and remove from the job queue.
        Remove from the gpu_free queue.
        """
        if not gpu_free.is_empty():
            job_to_run = job_queue.get()
            job_to_run.gpu = gpu_free.get()
            # Run the subprocess
            job_to_run.proc = Popen(['python', 'neural_style.py', '--content', '%s' % job_to_run.path1, '--styles', <style file>, '--output', '%s' % job_to_run.path])

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
            if self.new_job_exists():
                self.create_job_and_queue()

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
                    self.send_completed_to_db(job_i)
                    break

            if exit_code != 0 and completed_job is not None:
                self.send_error_to_db(job_i)

if __name__ == '__main__':
    js = job_scheduler()
    js.main()
