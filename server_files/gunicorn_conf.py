# /path-to-your-project/gunicorn_conf.py
bind = 'unix:/home/<user>/djangollmapi/djangollmapi.sock'
worker_class = 'sync'
loglevel = 'debug'
accesslog = '/var/log/gunicorn/djangollmapi.log'
acceslogformat = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog = '/var/log/gunicorn/djangollmapi_error.log'
capture_output = True
workers = 1
