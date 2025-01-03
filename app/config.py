import os

class config(object):
    USER = os.environ.get("PG_USER", 'postgres')
    PASSWORD = os.environ.get("PG_PASSWORD", '123')
    HOST = os.environ.get("PG_HOST", 'localhost')
    PORT = os.environ.get("PG_PORT", '5432')
    DB_NAME = os.environ.get("PG_DB_NAME", 'Group-Manager')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
    SECRET_KEY = '123'
    SQLALCHEMY_TRACK_MODIFICATIONS = True