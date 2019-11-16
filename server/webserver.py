from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import json
from threading import Thread
import re
import math
from urllib.parse import urlparse, parse_qs, unquote


# Paths
ROOT = "/api/"
HELLO = ROOT + "Hello"


# Util
def parseRequest(url_string: str):
    url_string = unquote(url_string)
    parsed_url = urlparse(url=url_string)
    params = parse_qs(qs=parsed_url.query)
    return {
        "path": parsed_url.path,
        "params": params
    }


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class WebRouter:
    def get(self, path: str):
        request = parseRequest(path)
        if request['path'] == ROOT:
            return json.dumps(
                {
                    "code": 200
                }
            )
        elif request['path'] == HELLO:
            return json.dumps(
                {
                    "message": "Hello"
                }
            )
        else:
            return json.dumps(
                {
                    "code": 404
                }
            )

__router__ = WebRouter()

class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(code=200)
            self.send_header("Content-Type", "image/x-icon")
            self.end_headers()
        else:
            payload = __router__.get(self.path)
            self.send_response(code=200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", len(payload))
            self.end_headers()
            # Return response
            self.wfile.write(bytes(payload, encoding="utf-8"))


class WebServer(Thread):
    def __init__(self, host: str, port: int, name: str):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.name = name
        self.webServer = None

    def run(self):
        try:
            print("Starting {}...".format(self.name))
            self.webServer = ThreadingHTTPServer((self.host, self.port), WebHandler)
            print("{} listening on http://{}:{}".format(self.name, self.host, self.port))
            self.webServer.serve_forever()
        except Exception as e:
            print("Something went wrong in {}: {}".format(self.name, e))

    def end(self):
        if self.webServer:
            self.webServer.shutdown()
            self.webServer.server_close()
        self.join()
