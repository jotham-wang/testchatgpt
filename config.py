# -*- coding: utf-8 -*-

import os


# gunicron
gunicorn_worker_num = int(os.environ.get('gunicorn_worker_num', 2))
gunicorn_thread_num = int(os.environ.get('gunicorn_thread_num', 2))
gunicorn_max_requests = int(os.environ.get('gunicorn_max_requests', 10000))
gunicorn_max_requests_jitter = int(os.environ.get('gunicorn_max_requests_jitter', 500))
