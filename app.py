from http.server import HTTPServer
from socketserver import ThreadingMixIn
import logging

from src.handler import HTTPRequestHandler


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread"""


def main():
    PORT = 8080
    server = ThreadingHTTPServer(("", PORT), HTTPRequestHandler)
    try:
        print(f"Server running on port {PORT}")
        logging.basicConfig(level=logging.INFO)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        server.socket.close()


if __name__ == "__main__":
    main()
