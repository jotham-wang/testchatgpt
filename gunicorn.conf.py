# -*- coding: utf-8 -*-

from config import gunicorn_worker_num, gunicorn_thread_num, gunicorn_max_requests, gunicorn_max_requests_jitter


# https://docs.gunicorn.org/en/latest/settings.html#worker-processes
workers = gunicorn_worker_num  # 进程数
threads = gunicorn_thread_num  # 线程数
max_requests = gunicorn_max_requests
max_requests_jitter = gunicorn_max_requests_jitter

worker_connections = 2000  # 最大并发量
backlog = 64  # 等待服务的最大请求数量
timeout = 600  # 超时时间
daemon = True  # 是否后台运行
reload = False  # 代码变动时是否自动重启服务

loglevel = 'info'
accesslog = "log/access.log"
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s %(a)s'
errorlog = "log/debug.log"
pidfile = 'log/gunicorn.pid'

bind = '0.0.0.0:6666'  # 监听的 ip 与服务端口, `0.0.0.0` 表示所有 ip
