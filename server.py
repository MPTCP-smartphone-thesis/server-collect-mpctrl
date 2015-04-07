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
import cgi
import database
import http.server
import json
import re
import socketserver
import threading
import urllib

parser = argparse.ArgumentParser(description="HTTP server to collect data from MultiPathControl")
parser.add_argument("ip", help="IP address used by the server")
parser.add_argument("port", type=int, help="port the server will listen to")
parser.add_argument("ip_db", help="IP address used by MongoDB")
parser.add_argument("port_db", type=int, help="port the db listen to")
parser.add_argument("db_name", help="name of the database to connect to")

args = parser.parse_args()


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        http.server.HTTPServer.shutdown(self)


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def get_json_data(self):
        length = int(self.headers.get('content-length'))
        data_raw = self.rfile.read(length).decode("UTF-8").strip()
        data = json.loads(str(data_raw))
        return data


    def do_POST(self):
        if None != re.search('/startup', self.path):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'application/json':
                data = self.get_json_data()
                if db.insert_startup(data):
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.send_response(403)
                    self.end_headers()
        elif None != re.search('/handover', self.path):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'application/json':
                data = self.get_json_data()
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
