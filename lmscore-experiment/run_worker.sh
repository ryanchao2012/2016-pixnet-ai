#!/bin/sh
celery -A tasks worker --loglevel=WARN -c 10
