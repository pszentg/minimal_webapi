# Example web API
This is a minimal web API written in python.

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

## Implementation
The task was to write a small Web API that accepts integers and stores them in-memory, 
then you can query for the average of the integers sent, and the count of said integers.
 
I extended the required functionality with the possibility to submit floats and strings, 
and I store the values in-memory and in a MongoDB database. 
The count of the items are implemented using a defaultdict locally, which is more efficient than using a list
to track the incoming data as the complexity of getting the count for a specific item is O(1), while
in a list I would have to iterate through the list, which is O(n) complex.

## Possible improvements
* Adding some security around the DB. Replacing Flask with Django would allow me to do some of these things
without implementing them manually.
* Remove the secrets from server.py and store them in a config file. 
This, however would render you unable to run this project on your own, unless you have your own MongoDB access.