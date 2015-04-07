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

parser = argparse.ArgumentParser(description="HTTP server to collect data from MultiPathControl")
parser.add_argument("ip", help="IP address used by the server")
parser.add_argument("port", type=int, help="port the server will listen to")

args = parser.parse_args()


def convert(data):
    ret = {}
    for k, v in data.items():
        k_dec = k.decode()
        v_dec = v[0].decode()
        ret[k_dec] = v_dec
    return ret


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if None != re.search('/startup', self.path):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.get('content-length'))
                data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                data = convert(data)
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
                data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                data = convert(data)
                print(data)
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
            self.wfile.write(bytes(json.dumps({3: 4}), 'UTF-8'))

        return

Handler = HTTPRequestHandler

httpd = socketserver.TCPServer((args.ip, args.port), Handler)
db = database.Database("127.0.0.1", 27017, "test")
httpd.serve_forever()
