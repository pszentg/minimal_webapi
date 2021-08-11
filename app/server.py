import json
import logging
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from numpy import mean

from ledger import Ledger

logger = logging.getLogger()

app = Flask(__name__)
app.config["MONGO_URI"] = \
    "mongodb+srv://user:HcSrNasKdaBBwJ0z@cluster0.wyb5l.mongodb.net/minimal_webapi?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

# create a ledger that locally tracks the values
ledger = Ledger()


# if i tracked only 1 type, eg. int, I'd only keep this route, and allow GET for queries.
# still would be possible if I sent a body with the GET request, but not a good practice
@app.route('/', methods=['POST'])
def receive():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    entry = {'value': payload}
    # insert into corresponding table/ledger depending on the type of value
    if type(payload) is int:
        ledger.ints[payload] += 1
        db.ints.insert_one(entry)
    elif type(payload) is float:
        ledger.floats[payload] += 1
        db.floats.insert_one(entry)
    elif type(payload) is str:
        ledger.strings[payload] += 1
        db.strings.insert_one(entry)
    else:
        raise TypeError("Unknown data type")

    return jsonify(success=True)


@app.route('/query_count', methods=["POST"])
def query_count():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    print(f'{payload} was submitted {ledger.get_count(payload)} according to the ledger')
    # because of the defaultdicts I don't have to worry about getting a KeyError here
    if type(payload) is int:
        collection = db.ints.find()
        ints = [item for item in collection]
        query = [item for item in ints if item['value'] == payload]
        print(f'{payload} was submitted {len(query)} times since the DB was initialized last.')

        # return jsonify({'payload': ledger.get_count(payload)}), 200
        return jsonify({'payload': len(query)}), 200

    if type(payload) is float:
        collection = db.floats.find()
        floats = [item for item in collection]
        query = [item for item in floats if item['value'] == payload]
        print(f'{payload} was submitted {len(query)} times since the DB was initialized last.')

        # return jsonify({'payload': ledger.get_count(payload)}), 200
        return jsonify({'payload': len(query)}), 200

    if type(payload) is str:
        collection = db.strings.find()
        ints = [item for item in collection]
        query = [item for item in ints if item['value'] == payload]
        print(f'{payload} was submitted {len(query)} times since the DB was initialized last.')

        # return jsonify({'payload': ledger.get_count(payload)}), 200
        return jsonify({'payload': len(query)}), 200


@app.route('/query_avg', methods=["POST"])
def query_avg():
    content = request.get_json()
    data = json.loads(content)
    payload = data['payload']
    if payload == 'int':
        collection = db.ints.find()
        ints = [item['value'] for item in collection]

        # using numpy.mean() in case the db gets too large for statistics.mean()
        return jsonify({'payload': mean(ints)}), 200
        # return jsonify({'payload': ledger.get_avg('ints')}), 200

    if payload == 'float':
        collection = db.floats.find()
        floats = [item['value'] for item in collection]

        # using numpy.mean() in case the db gets too large for statistics.mean()
        return jsonify({'payload': mean(floats)}), 200
        # return jsonify({'payload': ledger.get_avg('floats')}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

