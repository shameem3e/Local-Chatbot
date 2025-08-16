from pathlib import Path
from tinydb import TinyDB, Query

from backend.config.backend_config import backend_settings


# Initialize the database
DB_PATH = Path(backend_settings.DB_PATH)
db = TinyDB(DB_PATH)
conversations = db.table('conversations')
Q = Query()


class ChatStore:
    def __init__(self, conversations):
        self.conversations = conversations

chat_store = ChatStore(conversations)
