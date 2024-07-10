import logging
from celery import shared_task
from celery.utils.log import get_task_logger
import functools
from django.conf import settings

logger = get_task_logger(__name__)


@functools.cache
def get_factor():
    logging.info('getting factor')
    return 5


@shared_task(queue='serial')
def prove_singleton(x):
    logging.info("running prove_singleton")
    f = get_factor()
    return f * x


@functools.cache
def get_algorithm_instance():
    module = __import__(settings.LLM_PACKAGE)
    return module.Algorithm(logger=logger, model_names=settings.LLM_MODELS)


@shared_task(queue='serial')
def api_run(input_text):
    result = get_algorithm_instance().run(input_text)
    return result
