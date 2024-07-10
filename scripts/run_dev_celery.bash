#!/bin/bash

DJANGO_LLM_API_CONFIG=/Users/ms/.djangollmapi
EAGER_CELERY=false
celery -A djangollmapi  worker -E -l DEBUG -Q serial
