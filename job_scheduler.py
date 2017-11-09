import queue, sqlite3, logging, os, sys
from subprocess import Popen

"""
A job that contains information about the POST request.
Required information:

job_id : int
path1 : str
path2 : str
out : str
content_weight : float
content_blend : float
style_weight : float
style_scale : float
style_layer_weight_exp : float
preserve_color : bool

"""
class job(object):
    def __init__(self,
                 entry_id,
                 path_to_im1,
                 path_to_im2,
                 output_path,
                 content_weight,
                 content_blend,
                 style_weight,
                 style_scale,
                 style_layer_weight_exp,
                 iterations,
                 preserve_colors):

        self.job_id = entry_id
        self.path1 = path_to_im1
        self.path2 = path_to_im2
        self.out = output_path
        self.content_weight = content_weight
        self.content_blend = content_blend
        self.style_weight = style_weight
        self.style_scale = style_scale
        self.style_layer_weight_exp = style_layer_weight_exp
        self.preserve_colors = preserve_colors

        if (iterations < 5000):
            self.iterations = iterations
        else:
            self.iterations = 5000
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
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
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
        self.gpu_free = queue.Queue()
        self.running_jobs = []
        self.job_queue = queue.Queue()

        try:
            self.db = sqlite3.connect(name_db)
        except Exception as e:
            print(e)
            sys.exit()

        # Assuming that the gpu ranges from 0 to num_gpus - 1
        # gpu_0, gpu_1, etc.
        for i in range(num_gpus):
            self.gpu_free.put(i)

    def create_jobs_and_queue(self):
        """
        Retrieve the unqueued jobs, create job objects and queue them
        to the job_queue. Modify the job as 'queued' in the database.
        """
        c = self.db.cursor()
        new_job_exists = False
        ROWS = c.execute("SELECT * FROM deepstyle_job WHERE job_status='Q'")

        # checking
        if len(c.fetchall()) == 0:
            print("cannot find any jobs")

        for row in ROWS:
            self.job_queue.put(job(entry_id=c.lastrowid,
                              path_to_im1=row['input_image'].image_path.url,
                              path_to_im2=row['style_image'].image_path.url,
                              output_path=row['output_image'].image_path.url,
                              content_weight=row['content_weight'],
                              content_blend=row['content_weight_blend'],
                              style_weight=row['style_weight'],
                              style_scale=row['style_scale'],
                              style_layer_weight_exp=row['style_layer_weight_exp'],
                              iterations=row['iterations'],
                              preserve_colors=row['preserve_colors'])
                          )

            # Set queue status of current row's id to be 'queued'
            c.execute("UPDATE deepstyle_job SET job_status='P' WHERE rowid = %d" % c.lastrowid)
            new_job_exists = True
            self.logger.log.info("Job %d set In Progress" % c.lastrowid)
            print("ran create")
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
        if not gpu_free.empty():
            job_to_run = self.job_queue.get()
            job_to_run.gpu = gpu_free.get()

            # Create a copy of the environemnt
            new_env = os.environ.copy()
            new_env['CUDA_VISIBLE_DEVICES'] = str(job_to_run.gpu)

            # set preserve colors if indicated
            # assuming that preserve_colors will be of type boolean
            if job_to_run.preserve_colors:
                preserve = ''
            else:
                preserve = '--preserve-colors'

            # Run the subprocess
            job_to_run.proc = Popen(['python',
                                     'neural_style.py',
                                     '--content', '%s' % job_to_run.path1,
                                     '--styles', '%s' % job_to_run.path2,
                                     '--output','%s' % job_to_run.out,
                                     '--content-weight', job_to_run.content_weight,
                                     '--content-weight-blend', job_to_run.content_blend,
                                     '--style-weight', job_to_run.style_weight,
                                     '--style-layer-weight-exp', job_to_run.style_layer_weight_exp,
                                     '--style-scales', job_to_run.style_scale,
                                     '--iterations', job_to_run.iterations,
                                     '%s' % preserve
                                     ], env=new_env)

            self.logger.log.info("Job %d assigned GPU %d." % (job_to_run.job_id, job_to_run.gpu))
            print("ran assign")
            # Append the job to the running_job list
            running_procs.append(job_to_run)

    def main(self):
        """
        Create a pool of processes equivalent to the number of gpus
        Need async multiprocessing here...
        """
        while True:
            # When a new job exists in the database, create a job and load
            # into the job queue.
            self.create_jobs_and_queue()

            # When a job exists in the job queue
            if not self.job_queue.empty():
                while not gpu_free.empty():
                    self.assign_gpu_and_run()

            # Check the processes that are running
            # If proccesses are still running then this loop will continue to
            # run until a process is finished. Once a process has finished,
            # we can check if any requests are made and then create jobs from
            # them and we can check if any jobs are waiting. GPU bound.
            completed_job = None
            c = self.db.cursor()
            exit_code = 0
            for job_i in self.running_jobs:
                exit_code = job_i.proc.poll()
                if exit_code is not None:
                    completed_job = running_procs.remove(job_i)
                    gpu_free.put(completed_job.gpu)

                    # Change status of job in database
                    c.execute("UPDATE deepstyle_job SET job_status='C' WHERE rowid = %s" % c.lastrowid)

                    self.logger.log.info(job_i)
                    break

            if exit_code != 0 and completed_job is not None:
                print("Error in Popen")
                c.execute("UPDATE deepstyle_job SET job_status='F' WHERE rowid = %s" % c.lastrowid)
                self.logger.log.error(job_i)

            # close cursor
            c.close()

if __name__ == '__main__':

    js = job_scheduler(num_gpus=int(sys.argv[1]), name_db=sys.argv[2])

    js.main()
