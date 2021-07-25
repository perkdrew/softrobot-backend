from http.server import BaseHTTPRequestHandler
from urllib import parse
import functools, logging, json
from datetime import datetime

from .utils.config import Session, cache
from . import db


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/login"):
            user_id = int(self.path.split("/")[1])
            session = Session(user_id)
            if cache != {} and user_id == cache["session"]["user_id"]:
                logging.info(f"The user id {user_id} already exists.")
                session_key = session.get_session_key()
            else:
                session_key = session.create_session()
            return self.write_response(data=str({"user": session_key}))

        if self.path.endswith("/highscorelist"):
            level_id = int(self.path.split("/")[1])
            queryset = db.get_high_score_list(level_id, db.store)
            return self.write_response(data=queryset)

    def do_POST(self):
        url = parse.urlparse(self.path).query
        session_key = parse.parse_qs(url)["sessionkey"].pop()
        if cache != {} and cache["session"]["session_key"] == session_key:
            session = cache["session"]
            if datetime.utcnow() <= session["exp"]:
                level_id = int(self.path.split("/")[1])
                length = int(self.headers.get("Content-Length"))
                body = json.loads(self.rfile.read(length))
                logging.info(f"POST body: {body}")
                response = db.add_scores(
                    level_id, body["score"], session["user_id"], db.store
                )
                return self.write_response(response)
            else:
                return self.send_error(code=400, message="Token is expired or invalid.")
        else:
            return self.send_error(code=400, message="Authentication required.")

    @functools.lru_cache(maxsize=5)
    def write_response(self, data, status=200, content_type="application/json"):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        self.wfile.flush()
