import random
import requests
import json
import time

data = {"payload": 1}
data_json = json.dumps(data)
requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})

data = {"payload": 1.0}
data_json = json.dumps(data)
requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})

message = f"time:{time.time()}"
data = {"payload": message}
data_json = json.dumps(data)
requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})

r = requests.get("http://127.0.0.1:5000/count/1")
print(f'response for 1: {r.content}')

r = requests.get("http://127.0.0.1:5000/count/1.0")
print(f'response for 1.0: {r.content}')

r = requests.get(f"http://127.0.0.1:5000/count/{message}")
print(f'response for {message}: {r.content}')

# this is just for testing purposes
# data = {"payload": [1,2,3]}
# data_json = json.dumps(data)
# r = requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})
# print(r)

for i in range(5):
    data = {"payload": random.randint(0, 100)}
    data_json = json.dumps(data)
    requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})

r = requests.get("http://127.0.0.1:5000/avg/ints")
print(f'response for avg of ints: {r.content}')

for i in range(5):
    data = {"payload": random.random()*100}
    data_json = json.dumps(data)
    requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})


r = requests.get("http://127.0.0.1:5000/avg/floats")
print(f'response for avg of floats: {r.content}')
