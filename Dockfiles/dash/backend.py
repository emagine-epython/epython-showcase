"""
Used to update Redis in the backend.

Only need 1 instance running
"""

import redis
import os
import pickle
import time

if __name__ == '__main__':
    host = os.environ.get('REDIS_HOST', '127.0.0.1')
    port = os.environ.get('REDIS_PORT', '6379')
    r = redis.Redis(host=host, port=port)
    
    r.set('tick', 0)
    while True:
        time.sleep(1)
        r.incr('tick', 1)
        print(int(r.get('tick')))
