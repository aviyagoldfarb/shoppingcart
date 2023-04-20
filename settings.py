from datetime import timedelta

SECRET_KEY = "secret_key"
PERMANENT_SESSION_LIFETIME = timedelta(seconds=15)

SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False
