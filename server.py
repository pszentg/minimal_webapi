import math
import sqlite3 as sql
from collections import defaultdict

from flask import Flask, request, jsonify
import json

app = Flask(__name__)
# create tables if they don't exist
with sql.connect('database.db') as con:
    try:
        con.execute('CREATE TABLE ints (value INT)')
        con.execute('CREATE TABLE floats (value FLOAT)')
        con.execute('CREATE TABLE strings (value TEXT)')
    except sql.OperationalError:
        print('tables already exist')

# create a ledger that locally tracks the values
ledger = {"strings": defaultdict(int),
          "ints": defaultdict(int),
          "floats": defaultdict(int)}


# if i tracked only 1 type, eg. int, I'd only keep this route, and allow GET for queries.
# still would be possible if I sent a body with the GET request, but not a good practice
@app.route('/', methods=['POST'])
def receive():
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        conn.row_factory = sql.Row
        try:
            content = request.get_json()
            data = json.loads(content)
            payload = data['payload']

            # insert into corresponding table depending on the type of value
            if type(payload) is int:
                cur.execute("INSERT INTO ints (value) VALUES(?)", (payload,))
                ledger['ints'][payload] += 1

            elif type(payload) is float:
                cur.execute("INSERT INTO floats (value) VALUES(?)", (payload,))
                ledger['floats'][payload] += 1

            elif type(payload) is str:
                cur.execute("INSERT INTO strings (value) VALUES(?)", (payload,))
                ledger['strings'][payload] += 1

            else:
                raise TypeError("Unknown data type")

            return jsonify(success=True)

        except Exception as e:
            conn.rollback()
            print(e)
            return jsonify(success=False), 502


@app.route('/query_count', methods=["POST"])
def query_count():
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        conn.row_factory = sql.Row
        try:
            content = request.get_json()
            data = json.loads(content)
            payload = data['payload']
            if type(payload) is int:
                print(f'{payload} was submitted {ledger["ints"][payload]} times in this session')
                # this currently does not work as expected
                # total = cur.execute(f"SELECT * FROM ints WHERE value = {payload}").rowcount
                return jsonify({'payload': ledger["ints"][payload]}), 200

            if type(payload) is float:
                print(f'{payload} was submitted {ledger["floats"][payload]} times in this session')
                # total = cur.execute(f"SELECT * FROM floats WHERE value = {payload}").rowcount
                return jsonify({'payload': ledger["ints"][payload]}), 200

            if type(payload) is str:
                print(f'{payload} was submitted {ledger["strings"][payload]} times in this session')
                # total = cur.execute(f"SELECT * FROM strings WHERE value = {payload}").rowcount
                return jsonify({'payload': ledger["ints"][payload]}), 200

        except Exception as e:
            conn.rollback()
            print(e)
            return jsonify(success=False), 404


@app.route('/query_avg', methods=["POST"])
def query_avg():
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        conn.row_factory = sql.Row
        try:
            content = request.get_json()
            data = json.loads(content)
            payload = data['payload']
            if payload == 'int':
                # calculate avg of recorded ints in the db
                total = 0
                cur.execute("SELECT * FROM ints")
                for row in cur.fetchall():
                    total += row[0]
                cur.execute("SELECT Count() FROM ints")
                number_of_rows = cur.fetchone()[0]
                avg = math.floor(total/number_of_rows)

                # calculate the avg in the ledger
                total_nodb = 0
                for k, v in ledger['ints'].items():
                    total_nodb += int(k)*int(v)
                print(f'avg of ints: {math.floor(total_nodb/len(ledger["ints"]))}')

                return jsonify({'payload': avg}), 200

            if payload == 'float':
                total = 0.0
                cur.execute("SELECT * FROM floats")
                for row in cur.fetchall():
                    total += row[0]
                cur.execute("SELECT Count() FROM ints")
                number_of_rows = cur.fetchone()[0]
                avg = total / number_of_rows

                total_nodb = 0
                for k, v in ledger['floats'].items():
                    total_nodb += float(k)*float(v)
                print(f'avg of floats: {total_nodb/len(ledger["floats"].items())}')

                return jsonify({'payload': avg}), 200

        except Exception as e:
            conn.rollback()
            print(e)
            return jsonify(success=False), 404


if __name__ == '__main__':
    app.run(debug=True)
