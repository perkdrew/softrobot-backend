import random, string
from datetime import timedelta, datetime


class SessionStore:
    def __init__(self):
        self.store = {}

    def create_session(self, user_id: int, minutes: int = 10):
        self.exp = datetime.utcnow() + timedelta(minutes=minutes)
        self.session_key = "".join(
            random.choices(string.ascii_letters + string.digits, k=16)
        )
        self.store = {
            "user_id": user_id,
            "session_key": self.session_key,
            "exp": self.exp,
        }
        return self.session_key

    def get_session_key(self, user_id: int):
        if self.store["user_id"] == user_id:
            return self.store["session_key"]


session = SessionStore()
