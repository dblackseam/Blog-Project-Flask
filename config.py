import os


class Config:
    """ Flask app configuration. """
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL1", 'sqlite:///../db/blog.db')
