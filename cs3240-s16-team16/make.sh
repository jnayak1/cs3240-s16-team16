#!/bin/bash
rm -rf db.sqlite3
python manage.py syncdb
python manage.py makemigrations
python manage.py migrate
