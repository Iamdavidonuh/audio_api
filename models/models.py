from datetime import datetime
from .db import db

class CustomListField(db.ListField):
    def __init__(self, max_length=None,  **kwargs):
        self.max_length = max_length
        super(CustomListField, self).__init__(**kwargs)

    def validate(self, value):
        super(CustomListField, self).validate(value)

        if self.max_length is not None and len(value) > self.max_length:
            self.error('Too many items in the list')


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