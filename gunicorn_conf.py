import multiprocessing
import os

# Gunicorn config
bind = "0.0.0.0:8443"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
errorlog = "gunicorn-error.log"
accesslog = "gunicorn-access.log"
loglevel = "info"

# SSL Configuration
certfile = "cert.pem"
keyfile = "key.pem"

# Timeout configuration
timeout = 120
graceful_timeout = 120
