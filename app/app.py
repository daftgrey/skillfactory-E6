
import os
import logging
import redis
from flask import Flask, jsonify

app = Flask(__name__)

redis_config = {
    'host': os.environ.get('REDIS_HOST'),
    'port': os.environ.get('REDIS_PORT'),
    'db': 0,
}

logger = logging.getLogger('api-logger')
logger.setLevel(logging.INFO)
redis_client = redis.StrictRedis(**redis_config)


@app.route("/<number>", methods=['GET'])
def get_fibonacci_api(number):
    number = int(number)
    stored_value = redis_client.get(number)
    if stored_value:
        logger.info("For %s stored value is used" % number)
        return jsonify({number: stored_value.decode()}), 200
    new_value = get_fibonacci(number)
    logger.info("For %s new value is calculated" % number)
    redis_client.set(number, new_value)
    return jsonify({number: new_value}), 200


def get_fibonacci(number):
    if (number == 0) or (number == 1):
        return number
    return get_fibonacci(number-1) + get_fibonacci(number-2)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
