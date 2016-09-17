# You should most definitely run this from within a docker container, so you
# don't have library conflicts with other apps on the same system.
#

.DEFAULT_GOAL = docker-build

SHELL:=/bin/bash

# Darwin, Linux, Windows_NT
UNAME_S:=$(OS)
ifneq ($(OS),Windows_NT)
    UNAME_S:=$(shell uname -s)
endif

# The future
docker-build: clean init
	docker build -t python-ml-microservice .

docker-run: clean
	docker run -p 8080:8080 -it python-ml-microservice

run:
	cd app && uwsgi --http 0.0.0.0:8080 --wsgi-file app.py --callable app --master --enable-threads

clean:
	find . -name '*.pyc' -delete; \
	find . -name '*.log' -delete
	rm -rf ~/.cache/pip

init:
	virtualenv env
	./env/bin/pip install docker-compose

# Deprecated
install: requirements.txt
	pip install -r requirements.txt | grep -v "Requirement already satisfied" ; test $${PIPESTATUS[0]} -eq 0

setup: install
	pre-commit install

