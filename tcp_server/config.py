import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv("SERVER_HOST", "localhost")
    PORT = int(os.getenv("SERVER_PORT", 5000))
    MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", 5))
    BUFFER_SIZE = int(os.getenv("BUFFER_SIZE", 1024))