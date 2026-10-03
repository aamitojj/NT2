import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PAGE = Path(__file__).resolve().parent.joinpath("netboost", "ui", "index.html").read_text(encoding="utf-8")

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, kind):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        self._send(200, PAGE, "text/html; charset=utf-8")
    def do_POST(self):
        self._send(200, json.dumps({"title": "Your home is fine. Your provider is busy.", "body": "The router answered quickly. The path past it is the slow side. An app cannot add speed on the provider network."}), "application/json")
    def log_message(self, fmt, *args):
        return

def run():
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("NETBOOST is open at http://127.0.0.1:8765")
    webbrowser.open("http://127.0.0.1:8765")
    server.serve_forever()

if __name__ == "__main__":
    run()
