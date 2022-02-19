import os
bind = "127.0.0.1:8888"
logfile = os.path.dirname(os.path.realpath(__file__)) + "/gunicorn.log"
workers = 9