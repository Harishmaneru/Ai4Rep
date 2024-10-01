import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"  # Comment this out or remove it
timeout = 120


#bind = "0.0.0.0:443"
#workers = 3
#certfile = "/home/ubuntu/ssl_certs/fullchain.pem"
#keyfile = "/home/ubuntu/ssl_certs/onepgr.com.key"
