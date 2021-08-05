# Example web API
This is a minimal web API written in python.

## Requirements
requirements.txt is available, you can install the dependencies using `pip install -r requirements.txt` in the project root.

## Usage
Run the server from the project root using `python3 server.py`. After that you can interact 
with the server with the provided `send.py` script that does a few pre-defined interactions with the app.

## Implementation
The task was to write a small Web API that accepts integers and stores them in-memory, 
then you can query for the average of the integers sent, and the count of said integers.
 
I extended the required functionality with the possibility to submit floats and strings, and I store the values in-memory and in a 
SQLite database. The count of the items are implemented using a defaultdict locally, which is more efficient than using a list
to track the incoming data as the complexity of getting the count for a specific item is O(1), while
in a list I would have to iterate through the list, which is O(n) complex.

## Future improvements
* Due to time management issues I couldn't make sure querying the count of items from the database currently work as expected.
It needs some debugging.
* Adding a Dockerfile to make the app self-contained
* Adding some security around the DB. Replacing Flask with Django would allow me to do some of these things
without implementing them manually.