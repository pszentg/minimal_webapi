import random
import requests
import json

data = {"payload": 1}
data_json = json.dumps(data)
requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})

data = {"payload": 1.0}
data_json = json.dumps(data)
requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})

data = {"payload": "mystring"}
data_json = json.dumps(data)
requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})

data = {"payload": 1}
data_json = json.dumps(data)
r = requests.post("http://127.0.0.1:5000/count", json=data_json, headers={'Content-type': 'application/json'})
print(r.content)

data = {"payload": 1.0}
data_json = json.dumps(data)
r = requests.post("http://127.0.0.1:5000/count", json=data_json, headers={'Content-type': 'application/json'})
print(r.content)

data = {"payload": "mystring"}
data_json = json.dumps(data)
r = requests.post("http://127.0.0.1:5000/count", json=data_json, headers={'Content-type': 'application/json'})
print(r.content)

# this is just for testing purposes
# data = {"payload": [1,2,3]}
# data_json = json.dumps(data)
# r = requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})
# print(r)

for i in range(5):
    data = {"payload": random.randint(0, 100)}
    data_json = json.dumps(data)
    requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})

data = {"payload": 'int'}
data_json = json.dumps(data)
r = requests.post("http://127.0.0.1:5000/avg", json=data_json, headers={'Content-type': 'application/json'})
print(r.content)

for i in range(5):
    data = {"payload": random.random()*100}
    data_json = json.dumps(data)
    requests.post("http://127.0.0.1:5000", json=data_json, headers={'Content-type': 'application/json'})

data = {"payload": 'float'}
data_json = json.dumps(data)
r = requests.post("http://127.0.0.1:5000/avg", json=data_json, headers={'Content-type': 'application/json'})
print(r.content)


