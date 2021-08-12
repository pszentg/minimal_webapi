# Example web API
This is a minimal web API written in python. It can accept integers, floats and strings posted to it, store it in a 
MongoDB instance, and can return the count of specific items or the average (where applicable) of the items stored in the DB.

## Recommended usage
Docker is available for the project. If you have Docker and Docker Compose installed, navigate to the project root, and 
use `docker-compose up` to build and run the server. 

## Requirements locally
requirements.txt is available, you can install the dependencies using `pip install -r requirements.txt` in the project root.

## Running locally
Run the server from the project root using `python3 server.py`. 

## Testing
Assuming you installed the requirements, you can interact with the server with 
the provided `send.py` script that does a few pre-defined interactions with the app.

## Design decisions
Optionally, you can start the server with the -l flag: `python3 server.py -l`, this makes the server use a Ledger instance. It implements a similar functionality, but without interacting with the DB (making the server stateful), tracking the values locally.
Storing and reading the values from the ledger reduces the processing complexity to O(1), as it stores them in a defaultdict instead of a list. This would not be an appropriate solution if the order of the requests matter.

## Possible improvements
* Adding some security around the DB. Replacing Flask with Django would allow me to do some of these things
without implementing them manually.
* Remove the secrets from server.py and store them in a config file. 
This, however would currently render you unable to run this project on your own, unless you have your own MongoDB access. A viable approach to this would be to create a local replica of my cloud hosted DB and interact with the original using the MongoDB Atlas public API.
* Move the app to Heroku. This would also serve a stepping stone to the issue above.
