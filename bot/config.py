import os
from dotenv import load_dotenv

load_dotenv()
class config(object):
    TOKEN = os.getenv('TOKEN')
    API = "https://b2f0-85-159-27-200.ngrok-free.app"
    