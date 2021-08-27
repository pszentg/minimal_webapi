import json
from logging.config import dictConfig
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from flask_caching import Cache
import argparse
import re

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
        'level': 'INFO',
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

mongo = PyMongo(app)
db = mongo.db

cache = Cache(app)

if args.ledger:
    app.logger.info('starting server with ledger instead of DB')
    from ledger import Ledger
    ledger = Ledger()


@app.route('/', methods=['POST'])
def receive():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    if args.ledger:
        try:
            ledger.insert(payload)
            app.logger.info(f'ledgers are after insert:\n{ledger.ints}\n{ledger.floats}\n{ledger.strings}')
        except TypeError:
            return jsonify('Unknown data type', success=False), 501

    else:
        entry = {'value': payload}
        # insert into corresponding table depending on the type of value
        if type(payload) is int:
            db.ints.insert_one(entry)
        elif type(payload) is float:
            db.floats.insert_one(entry)
        elif type(payload) is str:
            db.strings.insert_one(entry)
        else:
            return jsonify('Unknown data type', success=False), 501

    return jsonify(success=True)


@app.route('/count/<count_type>', methods=["GET"])
@cache.cached(10, "ledger")
def query_count(count_type):
    int_regex = r"\d+(?=\.)"
    float_regex = r"\d+\.\d+"

    if re.match(int_regex, count_type):
        query_type = 1
    elif re.match(float_regex, count_type):
        query_type = 1.0
    else:
        query_type = "string"

    if args.ledger:
        app.logger.info(f'ledgers are before query:\n{ledger.ints}\n{ledger.floats}\n{ledger.strings}')
        app.logger.info(f'{query_type} was submitted {ledger.get_count(count_type)} according to the ledger')
        return jsonify({'payload': ledger.get_count(query_type)}), 200

    else:
        query = {'value': query_type}
        results = None
        if type(query_type) is int:
            results = db.ints.count_documents(query)

        elif type(query_type) is float:
            results = db.floats.count_documents(query)

        elif type(query_type) is str:
            results = db.strings.count_documents(query)

        if results:
            app.logger.info(results)
            app.logger.info(f'{query_type} was submitted {results} times since the DB was initialized last.')
            return jsonify({'payload': results}), 200
        else:
            return jsonify(success=False), 500


@app.route('/avg/<avg_type>', methods=["GET"])
@cache.cached(10, "ledger")
def query_avg(avg_type):

    if args.ledger:
        if avg_type == 'ints':
            return jsonify({'payload': ledger.get_avg('ints')}), 200

        if avg_type == 'floats':
            return jsonify({'payload': ledger.get_avg('floats')}), 200
        return jsonify(succes=False), 500

    else:
        pipeline = [
            {"$group": {"_id": "1", "results": {"$avg": "$value"}}},
        ]

        if avg_type == 'ints':
            return jsonify({'payload': list(db.floats.aggregate(pipeline))[0]["results"]}), 200

        if avg_type == 'floats':
            return jsonify({'payload': list(db.floats.aggregate(pipeline))[0]["results"]}), 200

        else:
            return jsonify(success=False), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

