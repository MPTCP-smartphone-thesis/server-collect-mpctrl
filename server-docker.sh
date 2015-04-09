#!/bin/sh
$(dirname $0)/server.py -I $MONGO_PORT_27017_TCP_ADDR -P $MONGO_PORT_27017_TCP_PORT $@
