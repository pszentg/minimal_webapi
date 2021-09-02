from flask_pymongo import PyMongo
from flask import jsonify
import logging


class Atlas:
    def __init__(self, app):
        mongo = PyMongo(app)
        self.db = mongo.db

    def insert(self, payload):
        entry = {'value': payload}
        # insert into corresponding table depending on the type of value
        if type(payload) is int:
            self.db.ints.insert_one(entry)
        elif type(payload) is float:
            self.db.floats.insert_one(entry)
        elif type(payload) is str:
            self.db.strings.insert_one(entry)
        else:
            return jsonify('Unknown data type', success=False), 501
        return jsonify(success=True), 200

    def query_count(self, item, query_type):
        if type(query_type) is int:
            query = {'value': int(item)}
        elif type(query_type) is float:
            query = {'value': float(item)}
        else:
            query = {'value': item}

        results = None
        if type(query_type) is int:
            logging.debug(f'submitting ints query: {query}')
            results = self.db.ints.count_documents(query)

        elif type(query_type) is float:
            logging.debug(f'submitting floats query: {query}')
            results = self.db.floats.count_documents(query)

        elif type(query_type) is str:
            logging.debug(f'submitting strings query: {query}')
            results = self.db.strings.count_documents(query)

        if results:
            logging.info(f'{query_type} was submitted {results} times since the DB was initialized last.')
            return jsonify({'payload': results}), 200
        else:
            return jsonify(success=False), 500

    def query_avg(self, query_type):
        pipeline = [
            {"$group": {"_id": "1", "results": {"$avg": "$value"}}},
        ]

        if query_type == 'ints':
            return jsonify({'payload': list(self.db.floats.aggregate(pipeline))[0]["results"]}), 200

        if query_type == 'floats':
            return jsonify({'payload': list(self.db.floats.aggregate(pipeline))[0]["results"]}), 200

        else:
            return jsonify(success=False), 500
