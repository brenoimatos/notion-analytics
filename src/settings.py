import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TOKEN = os.getenv("NOTION_API_TOKEN")
    COOKIE = os.getenv("NOTION_COOKIE")


config = Settings()
