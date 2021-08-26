import json
import logging
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from flask_caching import Cache
import argparse

parser = argparse.ArgumentParser(description='Process some incoming HTTP requests.')
parser.add_argument('--ledger', '-l', help='Switches the server to store the data locally instead of a remote DB',
                    action='store_true')
args = parser.parse_args()

logger = logging.getLogger()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(__name__)
cache.init_app(app)
app.config["MONGO_URI"] = \
    "mongodb+srv://user:HcSrNasKdaBBwJ0z@cluster0.wyb5l.mongodb.net/minimal_webapi?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

if args.ledger:
    print('starting server with ledger instead of DB')
    from ledger import Ledger
    ledger = Ledger()


@app.route('/', methods=['POST'])
@Cache.cached(cache, timeout=50)
def receive():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    if args.ledger:
        if type(payload) is int:
            ledger.ints[payload] += 1
        elif type(payload) is float:
            ledger.floats[payload] += 1
        elif type(payload) is str:
            ledger.strings[payload] += 1
        else:
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


@app.route('/count', methods=["POST"])
@Cache.cached(cache, timeout=50)
def query_count():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    if args.ledger:
        print(f'{payload} was submitted {ledger.get_count(payload)} according to the ledger')
        return jsonify({'payload': ledger.get_count(payload)}), 200

    else:
        query = {'value': payload}
        if type(payload) is int:
            results = db.ints.count_documents(query)
            print(results)
            print(f'{payload} was submitted {results} times since the DB was initialized last.')
            return jsonify({'payload': results}), 200

        if type(payload) is float:
            results = db.floats.count_documents(query)
            print(results)
            print(f'{payload} was submitted {results} times since the DB was initialized last.')
            return jsonify({'payload': results}), 200

        if type(payload) is str:
            results = db.strings.count_documents(query)
            print(results)
            print(f'{payload} was submitted {results} times since the DB was initialized last.')
            return jsonify({'payload': results}), 200


@app.route('/avg', methods=["POST"])
@Cache.cached(cache, timeout=50)
def query_avg():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    if args.ledger:
        if payload == 'int':
            return jsonify({'payload': ledger.get_avg('ints')}), 200

        if payload == 'float':
            return jsonify({'payload': ledger.get_avg('floats')}), 200

    else:
        pipeline = [
            {"$group": {"_id": "1", "results": {"$avg": "$value"}}},
        ]

        if payload == 'int':
            return jsonify({'payload': list(db.floats.aggregate(pipeline))[0]["results"]}), 200

        if payload == 'float':
            return jsonify({'payload': list(db.floats.aggregate(pipeline))[0]["results"]}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

