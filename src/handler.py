from http.server import BaseHTTPRequestHandler
from urllib import parse
import functools, logging, json
from datetime import datetime

from .utils.config import session
from . import db


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/login"):
            try:
                user_id = int(self.path.split("/")[1])
                if session.store != {} and user_id == session.store["user_id"]:
                    logging.info(f"The user id {user_id} already exists.")
                    session_key = session.get_session_key(user_id)
                else:
                    session_key = session.create_session(user_id)
                return self.write_response(data=str({"user": session_key}))
            except:
                return self.send_error(code=400)

        if self.path.endswith("/highscorelist"):
            try:
                level_id = int(self.path.split("/")[1])
                queryset = db.get_high_score_list(level_id, db.store)
                return self.write_response(data=queryset)
            except:
                return self.send_error(code=400)

    def do_POST(self):
        try:
            url = parse.urlparse(self.path).query
            session_key = parse.parse_qs(url)["sessionkey"].pop()
            if session.store != {} and session.store["session_key"] == session_key:
                if datetime.utcnow() <= session.store["exp"]:
                    level_id = int(self.path.split("/")[1])
                    length = int(self.headers.get("Content-Length"))
                    body = json.loads(self.rfile.read(length))
                    logging.info(f"POST body: {body}")
                    db.add_scores(
                        level_id, body["score"], session.store["user_id"], db.store
                    )
                else:
                    return self.send_error(code=400, message="Token is expired or invalid.")
            else:
                return self.send_error(code=400, message="Authentication required.")
        except:
            return self.send_error(code=400)

    @functools.lru_cache(maxsize=4)
    def write_response(self, data, status=200, content_type="application/json"):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        self.wfile.flush()
