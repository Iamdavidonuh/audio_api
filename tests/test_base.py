import unittest
from app import app
from src.models.models import AudioBook, Song, Podcast
from mongoengine import connect, disconnect


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
       disconnect()
    
    def setUp(self):
        self.app = app.test_client()



class TestModelBase(unittest.TestCase):
    
    song_data = {
        "song_title":"don't wake me up",
        "song_duration":20000
    }

    podcast_data  = {
            "podcast_name": "Darknet Daries",
            "podcast_duration":410000,
            "host": "Jack Rhysider",
            "participants": ["aban", "ban", "can", "dan"]
        }
    # invalid because participants must not be more than 10
    podcast_data_invalid  = {
            "podcast_name": "Darknet Daries2",
            "podcast_duration":41000,
            "host": "Jack Rhysider",
            "participants": ["a", "cx", "b", "an", "c", "d", "a", "ax", "buster", "sa", "fail"]
        }
    
    audiobook_data = {
            "title": "12 rules of live",
            "narrator": "Jordan Peterson",
            "author": "Jordan Peterson",
            "duration": 200001
        }
    
    def _create_song(self):
        return Song(**self.song_data).save()

    def _create_podcast(self):
        return Podcast(**self.podcast_data).save()

    def _create_podcast_invalid(self):
        """
        creates podcast object with more than 10 participants
        """
        return Podcast(**self.podcast_data_invalid).save()

    def _create_audiobook(self):
        return AudioBook(**self.audiobook_data).save()