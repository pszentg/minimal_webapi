import json
import logging
import math
from collections import defaultdict
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from numpy import mean

logger = logging.getLogger()

app = Flask(__name__)
app.config["MONGO_URI"] = \
    "mongodb+srv://user:HcSrNasKdaBBwJ0z@cluster0.wyb5l.mongodb.net/minimal_webapi?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

# create a ledger that locally tracks the values
ledger = {"strings": defaultdict(int),
          "ints": defaultdict(int),
          "floats": defaultdict(int)}


# if i tracked only 1 type, eg. int, I'd only keep this route, and allow GET for queries.
# still would be possible if I sent a body with the GET request, but not a good practice
@app.route('/', methods=['POST'])
def receive():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    entry = {'value': payload}
    # insert into corresponding table depending on the type of value
    if type(payload) is int:
        ledger['ints'][payload] += 1
        db.ints.insert_one(entry)
    elif type(payload) is float:
        ledger['floats'][payload] += 1
        db.floats.insert_one(entry)
    elif type(payload) is str:
        ledger['strings'][payload] += 1
        db.strings.insert_one(entry)
    else:
        raise TypeError("Unknown data type")

    return jsonify(success=True)


@app.route('/query_count', methods=["POST"])
def query_count():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    # because of the defaultdicts I don't have to worry about getting a KeyError here
    if type(payload) is int:
        print(f'{payload} was submitted {ledger["ints"][payload]} times in this session.')
        collection = db.ints.find()
        ints = [item for item in collection]
        query = [item for item in ints if item['value'] == payload]
        print(f'{payload} was submitted {len(query)} times since the DB was initialized last.')

        # return jsonify({'payload': ledger["ints"][payload]}), 200
        return jsonify({'payload': len(query)}), 200

    if type(payload) is float:
        print(f'{payload} was submitted {ledger["floats"][payload]} times in this session')
        collection = db.floats.find()
        floats = [item for item in collection]
        query = [item for item in floats if item['value'] == payload]
        print(f'{payload} was submitted {len(query)} times since the DB was initialized last.')

        # return jsonify({'payload': ledger["ints"][payload]}), 200
        return jsonify({'payload': len(query)}), 200

    if type(payload) is str:
        print(f'{payload} was submitted {ledger["strings"][payload]} times in this session')
        collection = db.strings.find()
        ints = [item for item in collection]
        query = [item for item in ints if item['value'] == payload]
        print(f'{payload} was submitted {len(query)} times since the DB was initialized last.')

        # return jsonify({'payload': ledger["ints"][payload]}), 200
        return jsonify({'payload': len(query)}), 200


@app.route('/query_avg', methods=["POST"])
def query_avg():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    print(f'payload is :{payload}')
    total = 0
    if payload == 'int':
        collection = db.ints.find()
        ints = [item['value'] for item in collection]
        for k, v in ledger['ints'].items():
            total += int(k) * int(v)
        print(f'avg of ints: {math.floor(total / len(ledger["ints"]))}')

        # using numpy.mean() in case the db gets too large for statistics.mean()
        return jsonify({'payload': mean(ints)}), 200
        # return jsonify({'payload': mean(ledger["ints"])}), 200

    if payload == 'float':
        collection = db.floats.find()
        floats = [item['value'] for item in collection]

        for k, v in ledger['floats'].items():
            total += float(k) * float(v)
        print(f'avg of floats: {total / len(ledger["floats"].items())}')

        # using numpy.mean() in case the db gets too large for statistics.mean()
        return jsonify({'payload': mean(floats)}), 200
        # return jsonify({'payload': mean(ledger["ints"])}), 200


if __name__ == '__main__':
    app.run(debug=True)

