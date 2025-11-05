import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
preload_app = True
wsgi_app = "core.wsgi:application"
chdir = "/opt/render/project/src/backend"
accesslog = "-"
errorlog = "-"