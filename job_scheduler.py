import queue, psycopg2, logging, os, sys
from subprocess import Popen
from psycopg2 import extras

INPUT_FILE_PATH="/app/media"
OUTPUT_FILE_PATH="/app/media"
VGG_LOCATION="/app/neural-style/imagenet-vgg-verydeep-19.mat"
"""
A job that contains information about the POST request entry.

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
preserve_color : bool (0 or 1)
"""
class job(object):
    def __init__(self,
                 j_id,
                 im_name1,
                 im_name2,
                 output_name,
                 content_weight,
                 content_blend,
                 style_weight,
                 style_scale,
                 style_layer_weight_exp,
                 iterations,
                 preserve_color,
                 width):

        self.job_id = j_id
        self.path1 = "%s/%s" % (INPUT_FILE_PATH, im_name1)
        self.path2 = "%s/%s" % (INPUT_FILE_PATH, im_name2)
        self.output_path = "%s/job_%d.jpg" % (OUTPUT_FILE_PATH, j_id)
        self.content_weight = content_weight
        self.content_blend = content_blend
        self.style_weight = style_weight
        self.style_scale = style_scale
        self.style_layer_weight_exp = style_layer_weight_exp
        self.preserve_color = preserve_color
        self.width = width

        if (iterations < 2001):
            self.iterations = iterations
        else:
            self.iterations = 1000
        self.gpu = None
        self.proc = None
        self.finished = None

    def __str__(self):
        return "%s : %s : %s" % (self.path1, self.path2, self.output_path)

class logger(object):
    """
    Create a logger and write to console and a file named "js_logger.txt".
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

        self.log.addHandler(self.fh)
        self.log.addHandler(self.ch)

    def shutdown(self):
        logging.shutdown()

"""
Job scheduler queries a POST REQUEST entries from the database and creates jobs
sent to the queue. If there exists a free gpu, then we execute a job from the
queue in shell and place the job in CURRENT_RUNNING. The program will loop
checking if the process exited has an exit code. When the job returns an exit
code, it will be removed from the CURRENT_RUNNING list and the gpu number will
be added back into the gpu_free queue.
"""
class job_scheduler(object):
    def __init__(self, num_gpus):
        self.logger = logger()
        self.num_gpus = num_gpus
        self.gpu_free = queue.Queue()
        self.running_jobs = []
        self.job_queue = queue.Queue()

        try:
            # self.db = sqlite3.connect(name_db)
            self.db = psycopg2.connect("dbname='test_db' user='test' host='db' password='test'")
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
        c = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        new_job_exists = False
        c.execute("SELECT * FROM deepstyle_job WHERE job_status='Q'")

        row = c.fetchone()
        while row is not None:
            try:

                s = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

                #s.execute("SELECT * FROM deepstyle_image WHERE rowid= %s" % row['input_image_id'])
                #input_row = s.fetchone()
                #input_row_path = input_row['image_file']

                #s.execute("SELECT * FROM deepstyle_image WHERE rowid= %s" % row['style_image_id'])
                #style_row = s.fetchone()
                #style_row_path = style_row['image_file']

                self.job_queue.put(job(j_id=row['id'],
                                  im_name1= row['input_image'], #input_row_path,
                                  im_name2= row['style_image'], #style_row_path,
                                  output_name= row['output_image'],
                                  content_weight=row['content_weight'],
                                  content_blend=row['content_weight_blend'],
                                  style_weight=row['style_weight'],
                                  style_scale=row['style_scale'],
                                  style_layer_weight_exp=row['style_layer_weight_exp'],
                                  iterations=row['iterations'],
                                  preserve_color=row['preserve_color'],
                                  width=row['output_width'])
                              )

                # Set queue status of current row's id to be queued 'Q'.
                c.execute("UPDATE deepstyle_job SET job_status='P' WHERE rowid = %d" % row['id'])
                new_job_exists = True
                self.logger.log.info("Job %d set In Progress" % row['id'])


            except Exception as e:
                self.logger.log.error("Job %d could not be set In Progress" % row['id'])
                self.logger.log.exception(e)
                z = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
                z.execute("UPDATE deepstyle_job SET job_status='F' WHERE rowid = %d" % row['id'])

            row = c.fetchone()

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

        """
        if not self.gpu_free.empty():
            job_to_run = self.job_queue.get()
            job_to_run.gpu = self.gpu_free.get()

            # Create a copy of the environemnt
            new_env = os.environ.copy()
            new_env['CUDA_VISIBLE_DEVICES'] = str(job_to_run.gpu)

            params = ['python',
                      '/app/neural-style/neural_style.py',
                      '--content', '%s' % job_to_run.path1,
                      '--styles', '%s' % job_to_run.path2,
                      '--output','%s' % job_to_run.output_path,
                      '--content-weight', str(job_to_run.content_weight),
                      '--content-weight-blend', str(job_to_run.content_blend),
                      '--style-weight', str(job_to_run.style_weight),
                      '--style-layer-weight-exp', str(job_to_run.style_layer_weight_exp),
                      '--style-scales', str(job_to_run.style_scale),
                      '--iterations', str(job_to_run.iterations),
                      '--width', str(job_to_run.width),
                      '--network', VGG_LOCATION
                     ]
            # set preserve colors if indicated
            # assuming that preserve_colors will be of type boolean
            if job_to_run.preserve_color:
                params.append('--preserve-colors')

            # Run the subprocess
            try:
                job_to_run.proc = Popen(params, env=new_env)
                self.logger.log.info("Job %d assigned GPU %d." % (job_to_run.job_id, job_to_run.gpu))
                self.running_jobs.append(job_to_run)

            except Exception as e:
                self.logger.log.error("Job %d could not be assigned GPU %d." % (job_to_run.job_id, job_to_run.gpu))
                self.logger.log.exception(e)
                c = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
                c.execute("UPDATE deepstyle_job SET job_status='PF' WHERE rowid = %d" % job_to_run.job_id)
                self.gpu_free.put(job_to_run.gpu)


    def main(self):
        """
        The main method to run to check, assign and run jobs.
        """
        while True:
            # When a new job exists in the database, create a job and load
            # into the job queue.
            self.create_jobs_and_queue()

            # When a job exists in the job queue
            if not self.job_queue.empty():
                while not self.gpu_free.empty():
                    self.assign_gpu_and_run()

            completed_job = None
            c = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # Need to set exit code to 0 since if no job then we won't exec
            # the error handling and if there is a job it won't matter.
            exit_code = 0

            # Loop will run until a job is finished
            for job_i in self.running_jobs:

                # job.proc could be None if the process doesn't exist
                # but this is mitigated since no job in running_jobs will
                # ever have None in its proc attribute
                exit_code = job_i.proc.poll()
                if exit_code is not None:
                    completed_job = job_i
                    # It is okay to remove this job from running_jobs because it will
                    # break in this if statement anyways
                    self.running_jobs.remove(job_i)
                    self.gpu_free.put(completed_job.gpu)

                    # Change status of job in database
                    if (exit_code == 0):
                        c.execute("UPDATE deepstyle_job SET job_status='C' WHERE rowid = %s" % completed_job.job_id)

                    self.logger.log.info(str(job_i) + " Exit code: %d" % exit_code)
                    break

            # Completed_job only None if exit_code is None which means it's still running
            # If exit_code is not 0, then an error has occurred.
            if exit_code != 0 and completed_job is not None:

                # Remove job from executing by setting status to F
                c.execute("UPDATE deepstyle_job SET job_status='F' WHERE rowid = %s" % completed_job.job_id)
                self.logger.log.error(str(job_i) + " failed to complete.")

            # close cursor
            c.close()

if __name__ == '__main__':

    js = job_scheduler(num_gpus=int(sys.argv[1]))

    js.main()
