from flask import Flask
from redis import Redis
import os

redis = Redis(host=os.environ['REDIS_HOST'], port=6379)


def create_app():
    _app = Flask(__name__)

    @_app.route('/')
    def hello():
        redis.incr('hits')
        return 'Hello compose extends World!! ' \
               'I have been seen %s times.' % redis.get('hits')

    return _app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True)
