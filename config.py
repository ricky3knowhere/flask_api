import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    HOST = str(os.environ.get("DB_HOST"))
    DATABASE = str(os.environ.get("DB_DATABASE"))
    USERNAME = str(os.environ.get("DB_USERNAME"))
    PASSWORD = str(os.environ.get("DB_PASSWORD"))

    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET_KEY"))
    UPLOAD_FOLDER = str(os.environ.get("UPLOAD_FOLDER"))
    MAX_CONTENT_SIZE = 2 * 1024 * 1024

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
    SQLALCHEMY_TRACK_NOTIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
