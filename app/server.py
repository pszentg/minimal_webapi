import json
import argparse
import re
from logging.config import dictConfig
from flask import Flask, request, jsonify
from flask_caching import Cache
from app.atlas import Atlas

parser = argparse.ArgumentParser(description='Process some incoming HTTP requests.')
parser.add_argument('--ledger', '-l', help='Switches the server to store the data locally instead of a remote DB',
                    action='store_true')
args = parser.parse_args()

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

config = {
    "DEBUG": True,
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "MONGO_URI":
        "mongodb+srv://user:HcSrNasKdaBBwJ0z@cluster0.wyb5l.mongodb.net/minimal_webapi?retryWrites=true&w=majority"
}

app = Flask(__name__)
app.config.from_mapping(config)

db = Atlas(app)

cache = Cache(app)

if args.ledger:
    app.logger.info('starting server with ledger instead of DB')
    from ledger import Ledger
    ledger = Ledger()


@app.route('/', methods=['POST'])
def insert():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    if args.ledger:
        try:
            return ledger.insert(payload)
        except TypeError:
            return jsonify('Unknown data type', success=False), 501

    else:
        return db.insert(payload)


@app.route('/count/<item>', methods=["GET"])
@cache.cached(10)
def query_count(item):
    with app.app_context():
        cache.clear()
    int_regex = r"^[-+]?[0-9]+$"
    float_regex = r"^[-+]?[0-9]+\.[0-9]+$"

    if re.match(int_regex, item):
        query_type = 1
    elif re.match(float_regex, item):
        query_type = 1.0
    else:
        query_type = "string"

    if args.ledger:
        app.logger.debug(f'ledgers are before query:\n{ledger.ints}\n{ledger.floats}\n{ledger.strings}')
        app.logger.info(f'{query_type} was submitted {ledger.get_count(item)} according to the ledger')
        if type(query_type) is int:
            return jsonify({'payload': ledger.get_count(int(item))}), 200
        elif type(query_type) is float:
            return jsonify({'payload': ledger.get_count(float(item))}), 200
        else:
            return jsonify({'payload': ledger.get_count(item)}), 200

    else:
        return db.query_count(item, query_type)


@app.route('/avg/<avg_type>', methods=["GET"])
@cache.cached(10)
def query_avg(avg_type):
    with app.app_context():
        cache.clear()
    if args.ledger:
        if avg_type == 'ints':
            return jsonify({'payload': ledger.get_avg('ints')}), 200

        if avg_type == 'floats':
            return jsonify({'payload': ledger.get_avg('floats')}), 200
        return jsonify(succes=False), 500

    else:
        return db.query_avg(avg_type)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

