#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
#  Copyright 2015 Matthieu Baerts & Quentin De Coninck
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  To install: pymongo

import argparse
from pymongo import MongoClient

parser = argparse.ArgumentParser(description="HTTP server to collect data from MultiPathControl")
parser.add_argument("ip", help="IP address used by the server")
parser.add_argument("port", type=int, help="port the server will listen to")
parser.add_argument("db-name", help="name of the database to connect to")

STARTUP_KEYS = ["wifiMac", "timestamp", "versionName", "versionCode", "lastUpdate", "enable", "defRouteCell",
                "cellBackup", "saveBattery", "ipv6", "savePowerGPS", "TCPCCAlgo"]
HANDOVER_KEYS = ["wifiMac", "timestamp", "airplane", "cellBer", "cellSignal4", "cellSignaldBm",
                "dataActivity", "dataState", "cellType", "extIp", "gsmCellLac", "gsmFullCellId", "gsmRNC",
                "gsmShortCellId", "ifaces", "ipWifi4", "ipWifi6", "ipRMNet4", "ipRMNet6", "netstat",
                "netAvailable", "netConnected", "netDState", "netExtras", "netFailover", "netReason",
                "netRoaming", "netType", "posAccuracy", "posLatitude", "posLongitude", "posSpeed",
                "procMPTCP", "procMPTCPFM", "simOperator", "simState", "tracking", "wifiBSSID", "wifiFreq",
                "wifiSignal4", "wifiSignalRSSI", "wifiSpeed", "wifiSSID", "wifiState"]


class Database(object):
    def __init__(self, ip, port, db_name):
        self.connect_db(ip, port, db_name)

    def connect_db(self, ip, port, db_name):
        connection = MongoClient(host=ip, port=port)
        self.db = connection[db_name]

    def insert(self, data, collection):
        ret = collection.insert(data)
        return (ret is not None and ret != [None])

    def insert_in_collection(self, dico, collection, collection_keys):
        """ Returns True iff the element is inserted in db
        """
        if not set(dico.keys()).issubset(set(collection_keys)):
            return False
        return self.insert(dico, collection)

    def insert_startup(self, dico):
        return self.insert_in_collection(dico, self.db.startup, STARTUP_KEYS)

    def insert_handover(self, dico):
        return self.insert_in_collection(dico, self.db.handover, HANDOVER_KEYS)

if __name__ == "__main__":
    args = parser.parse_args()
    db = Database(args.ip, args.port, args.db_name)
