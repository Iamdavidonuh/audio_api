from datetime import datetime
from .db import db


class Song(db.Document):
    song_title = db.StringField(required=True, max_length=100)
    song_duration = db.IntField(required=True, min_value=0)
    uploaded = db.DateTimeField(required=True, default=datetime.utcnow)


class Podcast(db.Document):
    podcast_name = db.StringField(required=True, max_length=100)
    podcast_duration = db.IntField(required=True, min_value=0)
    uploaded = db.DateTimeField(required=True, default=datetime.utcnow)
    host = db.StringField(required=True, max_length=100)
    participants = db.ListField(db.StringField(max_length=100), max_length=10)


class AudioBook(db.Document):
    title = db.StringField(required=True,  max_length=100)
    duration = db.IntField(required=True, min_value=0)
    author = db.StringField(required=True,  max_length=100)
    narrator = db.StringField(required=True, max_length=100)
    uploaded = db.DateTimeField(required=True, default=datetime.utcnow)