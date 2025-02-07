import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits') 
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    # print the hostname and IP address of the container
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    count = get_hit_count()

    return_msg = (
        f"Hostname: {hostname}<br/>"
        f"IP Address: {ip_address}<br/>"
        f"I have been seen {count} times.<br/>"
    )
    return return_msg

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)