

# Bind IP address and port
bind = "127.0.0.1:8080"

# Set the number of worker processes, here set to twice the number of CPU cores
# workers = multiprocessing.cpu_count() * 2
workers = 2

# Set the worker class, default is 'sync', you can also choose 'gevent' (requires installing the gevent package)
# worker_class = 'sync'

# Set the worker timeout (in seconds)
# timeout = 30

# Set the log level, options include 'debug', 'info', 'warning', 'error', 'critical'
# loglevel = 'info'

# Set the error log file path
# errorlog = 'gunicorn_error.log'

# Set the access log file path
# accesslog = 'gunicorn_access.log'

# Set the access log format
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'