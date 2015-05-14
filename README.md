# server-collect-mpctrl

HTTP/REST server to collect data from MultiPathControl's Android application.

This Android app sends data to this server in a POST HTTP request and in JSON format. All data are added to a MongoDB database.

## How to launch it?

Simply launch `server.py` file. Here is optional arguments:

* `-i` or `--ip`: IP address bind by this server ; default: `0.0.0.0`
* `-p` or `--port`: port the server will listen to ; default: `1234`
* `-I` or `--ip_db`: IP address used by MongoDB server ; default: `127.0.0.1`
* `-P` or `--port_db`: port the DB listen to ; default: `27017`
* `-N` or `--db_name`: name of the database to connect to ; default: `mpctrl`
