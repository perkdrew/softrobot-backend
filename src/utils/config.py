import random, string
from datetime import timedelta, datetime


cache = {}


class Session:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def create_session(self, minutes: int = 10):
        self.exp = datetime.utcnow() + timedelta(minutes=minutes)
        self.session_key = "".join(
            random.choices(string.ascii_letters + string.digits, k=16)
        )
        self.session = {
            "user_id": self.user_id,
            "session_key": self.session_key,
            "exp": self.exp,
        }
        cache["session"] = self.session
        return self.session_key

    def get_session_key(self):
        if cache["session"]["user_id"] == self.user_id:
            return cache["session"]["session_key"]
