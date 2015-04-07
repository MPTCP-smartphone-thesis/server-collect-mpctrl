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

import argparse
import database
import cgi
import http.server
import json
import re
import socketserver
import threading

parser = argparse.ArgumentParser(description="HTTP server to collect data from MultiPathControl")
parser.add_argument("ip", help="IP address used by the server")
parser.add_argument("port", type=int, help="port the server will listen to")
parser.add_argument("ip_db", help="IP address used by MongoDB")
parser.add_argument("port_db", type=int, help="port the db listen to")
parser.add_argument("db_name", help="name of the database to connect to")

args = parser.parse_args()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def convert_value(v):
    if is_number(v):
        return float(v)
    elif v.startswith("[") and v.endswith("]"):
        v_list = []
        elements = v[1:-1].split(",")
        for element in elements:
            v_list.append(convert_value(element))
        return v_list
    elif v.lower() == "true":
        return True
    elif v.lower() == "false":
        return False
    else:
        return v


def convert(data):
    ret = {}
    for k, v in data.items():
        k_dec = k.decode()
        v_dec = convert_value(v[0].decode())
        ret[k_dec] = v_dec
    return ret

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        http.server.HTTPServer.shutdown(self)

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if None != re.search('/startup', self.path):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.get('content-length'))
                data_raw = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                # Needed because byte stream...
                data_string = list(data_raw.keys())[0].decode()
                data = json.loads(data_string)
                if db.insert_startup(data):
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.send_response(403)
                    self.end_headers()
        elif None != re.search('/handover', self.path):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.get('content-length'))
                data_raw = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                # Needed because byte stream...
                data_string = list(data_raw.keys())[0].decode()
                data = json.loads(data_string)
                if db.insert_handover(data):
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.send_response(403)
                    self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # self.wfile.write(bytes(json.dumps({3: 4}), 'UTF-8'))
        return

class SimpleHttpServer():
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def stop(self):
        self.server.shutdown()
        self.waitForThread()

server = SimpleHttpServer(args.ip, args.port)
db = database.Database(args.ip_db, args.port_db, args.db_name)
server.start()
server.waitForThread()
