#!flask/bin/python
import boto
from flask import Flask, jsonify, abort, request
from utils import config, logger
from TaskTracker import TaskTracker
from concurrent import futures
from ML import ML

app = Flask(__name__)

print 'Started the Python ML Microservice'

s3conn = boto.connect_s3(config["aws"]["AWS_ACCESS_KEY_ID"], config["aws"]["AWS_SECRET_ACCESS_KEY"])
bucket = s3conn.get_bucket(config["aws"]["BUCKET"])

# Feel free to increase the number of workers
executor = futures.ThreadPoolExecutor(max_workers=4)
task_tracker = TaskTracker()

# Download the given S3 object and process it
def downloadAndProcessFiles(s3files, action):
    for s3filename in s3files:
      # Construct a reference to the S3 object so we can download it.
      k = boto.s3.key.Key(bucket)
      k.key = s3filename

      try:
	  contents = k.get_contents_as_string()
      except:
	  print "Error: S3 couldn't download "+s3filename

      if (action == "train"):
	  ML.handleTrainFile(content)
      elif (action == "input"):
	  ML.handleInputFile(content)
      elif (action == "output"):
	  output = ML.handleOutputFile(content)
	  return output
      else:
	  # Doesn't make sense, it's got to be one of the three APIs
	  return False

      return True

@app.route('/')
@app.route('/index')
def index():
    return "Greetings from our python ML microservice."

# Handle a new /train request
@app.route('/train', methods=['POST'])
def train_handle():
    if not request.json:
        abort(500, "/train request body is not json")
    if not 'files' in request.json:
        abort(500, "/train request body missing files: [<s3 paths>, ...]")

    # This is the S3 key, e.g. deviceid/table/timestamp.csv
    s3files = request.json['files']

    # Enqueue a job on the thread pool to download and process the CSV
    future = executor.submit(downloadAndProcessFiles, s3files, "train")
    taskID = task_tracker.register_future(future)

    return jsonify({'jobId': str(taskID)}), 202

# Handle a new /input request
@app.route('/input', methods=['POST'])
def input_handle():
    if not request.json:
        abort(500, "/input request body is not json")
    if not 'files' in request.json:
        abort(500, "/input request body missing files: [<s3 paths>, ...]")

    # This is a list of S3 file paths relative to the bucket
    s3files = request.json['files']

    # Enqueue a job on the thread pool to download and process the CSV
    future = executor.submit(downloadAndProcessFiles, s3files, "input")
    taskID = task_tracker.register_future(future)

    return jsonify({'jobId': str(taskID)}), 202

# Handle a new /output request
@app.route('/output', methods=['POST'])
def output_handle():
    if not request.json:
        abort(500, "/output request body is not json")
    if not 'files' in request.json:
        abort(500, "/output request body missing files: [<s3 paths>, ...]")

    # This is the S3 key, e.g. deviceid/table/timestamp.csv
    s3files = request.json['files']

    # process synchronously, the server gives us threads either way
    result = downloadAndProcessFiles(s3files, "output")

    return jsonify({'output': result}), 200


