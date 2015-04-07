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

args = parser.parse_args()

WIFIMAC = "wifiMac"
DATA = "data"


class Database(object):
    def __init__(self, ip, port, db_name):
        self.connect_db(ip, port, db_name)

    def connect_db(self, ip, port, db_name):
        connection = MongoClient(host=ip, port=port)
        self.db = connection[db_name]

    def insert(self, data, collection):
        ret = collection.insert(data)
        return (ret != None and ret != [None])

    def insert_startup(self, dico):
        """ Returns the number of elements inserted in db
            If there is an error with insertion of one element, stop inserting following ones
        """
        wifimac = dico.get(WIFIMAC, None)
        if not wifimac:
            return 0
        count = 0
        for data in dico.get(DATA, []):
            data[WIFIMAC] = wifimac
            if not self.insert(data, db.startup):
                return count
            count += 1
        return count

    def insert_handover(self, dico):
        """ Returns the number of elements inserted in db
            If there is an error with insertion of one element, stop inserting following ones
        """
        wifimac = dico.get(WIFIMAC, None)
        if not wifimac:
            return 0
        count = 0
        for data in dico.get(DATA, []):
            data[WIFIMAC] = wifimac
            if not self.insert(data, db.handover):
                return count
            count += 1
        return count


db = Database(args.ip, args.port, args.db_name)
