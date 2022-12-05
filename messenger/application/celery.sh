#!/bin/bash
celery -A application worker -l INFO
celery -A application flower --port=5555 -l INFO
