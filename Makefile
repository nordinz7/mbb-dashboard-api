# Makefile for mbb-dashboard-api

.PHONY: run install lint test

install:
	pip install -r requirements.txt

run:
	FLASK_APP=app FLASK_ENV=development flask run

lint:
	flake8 app

test:
	pytest
