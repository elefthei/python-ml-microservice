import yaml, os, sys
import logging
import logging.handlers

# Utilities for logging, config etc.

# Silence boto
logging.getLogger('boto').setLevel(logging.CRITICAL)

# Set up a specific logger with our desired output level
logger = logging.getLogger('ml')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

# Add the log message handler to the logger

config = {}
with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

if 'RDS_HOSTNAME' in os.environ:
    thehostname = os.environ['RDS_HOSTNAME']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'postgresql',
            'PORT': '',
        }
    }
