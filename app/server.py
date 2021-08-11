import json
import logging
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from numpy import mean
import argparse

parser = argparse.ArgumentParser(description='Process some incoming HTTP requests.')
parser.add_argument('--ledger', '-l', help='Switches the server to store the data locally instead of a remote DB',
                    action='store_true')
args = parser.parse_args()

logger = logging.getLogger()

app = Flask(__name__)
app.config["MONGO_URI"] = \
    "mongodb+srv://user:HcSrNasKdaBBwJ0z@cluster0.wyb5l.mongodb.net/minimal_webapi?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

if args.ledger:
    print('starting server with ledger instead of DB')
    from ledger import Ledger
    ledger = Ledger()


@app.route('/', methods=['POST'])
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
def query_count():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    if args.ledger:
        print(f'{payload} was submitted {ledger.get_count(payload)} according to the ledger')
        return jsonify({'payload': ledger.get_count(payload)}), 200

    else:
        if type(payload) is int:
            collection = db.ints.find()
            query = [item for item in collection if item['value'] == payload]
            print(f'{payload} was submitted {len(query)} times since the DB was initialized last.')
            return jsonify({'payload': len(query)}), 200

        if type(payload) is float:
            collection = db.floats.find()
            query = [item for item in collection if item['value'] == payload]
            print(f'{payload} was submitted {len(query)} times since the DB was initialized last.')
            return jsonify({'payload': len(query)}), 200

        if type(payload) is str:
            collection = db.strings.find()
            query = [item for item in collection if item['value'] == payload]
            print(f'{payload} was submitted {len(query)} times since the DB was initialized last.')
            return jsonify({'payload': len(query)}), 200


@app.route('/avg', methods=["POST"])
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
        if payload == 'int':
            collection = db.ints.find()
            ints = [item['value'] for item in collection]

            # using numpy.mean() in case the db gets too large for statistics.mean()
            return jsonify({'payload': mean(ints)}), 200

        if payload == 'float':
            collection = db.floats.find()
            floats = [item['value'] for item in collection]

            return jsonify({'payload': mean(floats)}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

