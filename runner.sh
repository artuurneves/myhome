#!/bin/sh


python run.py db init
python run.py db migrate
python run.py db upgrade
python run.py runserver