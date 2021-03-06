from mongoengine.errors import ValidationError
from src.models.models import Song, Podcast, AudioBook
from tests.test_base import TestBase

class TestSongModel(TestBase):
    song_data = {
            "song_title":"don't wake me up",
            "song_duration":20000
    }
    def setUp(self):
        song = Song(**self.song_data).save()

    def test_song_object_creation(self):
        song = Song.objects.first()
        self.assertIsNotNone(song)
        self.assertEqual(song.song_title, self.song_data['song_title'])

class TestPodcastModel(TestBase):

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
    def setUp(self):
        podcast = Podcast(**self.podcast_data).save()

    def create_podcast_invalid(self):
        podcast = Podcast(**self.podcast_data_invalid).validate()
        return podcast

    def test_podcast_object_creation(self):
        podcast = Podcast.objects.first()
        self.assertIsNotNone(podcast)
        self.assertEqual(podcast.podcast_name, self.podcast_data['podcast_name'])
        self.assertEqual(podcast.host, self.podcast_data["host"])
        self.assertListEqual(podcast.participants, self.podcast_data["participants"])
    
    def test_podcast_object_creation_fails_extra_participants(self):
        """ tries to create a podcast object with more than 10 participants"""

        with self.assertRaises(ValidationError) as error:
            self.create_podcast_invalid()
            self.assertIn("List is too long", str(error))
        

class TestAudioBookModel(TestBase):
    audiobook_data = {
            "title": "12 rules of live",
            "narrator": "Jordan Peterson",
            "author": "Jordan Peterson",
            "duration": 200001
        }
    def setUp(self):
        audiobook = AudioBook(**self.audiobook_data).save()

    def test_audiobook_object_creation(self):
        audiobook = AudioBook.objects.first()
        self.assertIsNotNone(audiobook)
        self.assertEqual(audiobook.title, self.audiobook_data['title'])
        self.assertEqual(audiobook.narrator, self.audiobook_data['narrator'])
        self.assertEqual(audiobook.author, self.audiobook_data['author'])

