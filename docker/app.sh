#!/bin/bash

alembic upgrade head

cd src

python start_background_tasks.py
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
