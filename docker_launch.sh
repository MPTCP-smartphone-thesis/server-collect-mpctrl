#!/bin/bash
test "$1" != "" && MONGO=$1 || MONGO=mongo
shift
test "$1" != "" && PORT=$1 || PORT=1234
shift

docker run --name mpctrl --link $MONGO:mongo -d -P -p $PORT:1234 -v $(pwd)/server.py:/server-collect-mpctrl/server.py:ro -v $(pwd)/database.py:/server-collect-mpctrl/database.py:ro matttbe/mpctrl $@
