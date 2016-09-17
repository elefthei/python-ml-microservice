ML Microservice in Python
---------------------------

Simple uWSGI with Flask web server implementing our Machine Learning REST API.

## Introduction

Python obviously has some exceptional ML libraries. To facilitate using them I have
written a simple REST API that should work for most ML models, as well as a Docker container
around the whole thing.

## Usage

Edit app/config.yml to add your AWS credentials.
```
aws:
  BUCKET : '<bucker name>'
  AWS_ACCESS_KEY_ID : '<ACCESS_KEY_ID here>'
  AWS_SECRET_ACCESS_KEY : '<ACCESS_SECRET_KEY here>'
```

And to handle each file passed in the POST request, use app/ML.py:
```
  def handleTrainFile(contents):
    # Dear ML engineer, feel free to handle the training
    # of your model here.
    print 'Received /train file, contents...'
    print contents

```

## REST API

### POST /train

Body:
```
{
  files: [ <S3 file path>, ...]
}
```

Example:
```
{
  files: [ 32AD86AB68CB4368830506D352772A12/bluetooth/490569736771195.csv ]
}
```

Response:
```
{
  "jobId": "1"
}
```

Error: *500*

### POST /input

Body:
```
{
  files: [ <S3 file path>, ... ]
}
```
Response:
```
{
  "jobId": "1"
}
```
Error: *500*

### POST /output/

Body:
```
{
  files: [ <s3 file path>, ... ]
}

```

Response:
```
{
  output: { output vector }
}
```

Error: *500*

