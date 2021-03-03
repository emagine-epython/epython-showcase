"""
Used to update Redis in the backend.

Only need 1 instance running
"""

import redis
import pickle
import time
import kydb

if __name__ == '__main__':
    db = kydb.connect('dynamodb://epython')
    config = db['/demos/epython-dash-demo/config']
    
    host = config.get('REDIS_HOST', '127.0.0.1')
    port = config.get('REDIS_PORT', '6379')
    r = redis.Redis(host=host, port=port)
    
    r.set('tick', 0)
    while True:
        time.sleep(1)
        r.incr('tick', 1)
        print(int(r.get('tick')))
