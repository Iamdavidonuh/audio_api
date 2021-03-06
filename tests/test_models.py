from mongoengine.errors import ValidationError
from src.models.models import Song, Podcast, AudioBook
from tests.test_base import TestBase, TestModelBase

class TestSongModel(TestBase, TestModelBase):
    def setUp(self):
        self._create_song()

    def test_song_object_creation(self):
        song = Song.objects.first()
        self.assertIsNotNone(song)
        self.assertEqual(song.song_title, self.song_data['song_title'])

class TestPodcastModel(TestBase, TestModelBase):

    def setUp(self):
        self._create_podcast()

    def test_podcast_object_creation(self):
        podcast = Podcast.objects.first()
        self.assertIsNotNone(podcast)
        self.assertEqual(podcast.podcast_name, self.podcast_data['podcast_name'])
        self.assertEqual(podcast.host, self.podcast_data["host"])
        self.assertListEqual(podcast.participants, self.podcast_data["participants"])
    
    def test_podcast_object_creation_fails_extra_participants(self):
        """ tries to create a podcast object with more than 10 participants"""

        with self.assertRaises(ValidationError) as error:
            self._create_podcast_invalid()
            self.assertIn("List is too long", str(error))
        

class TestAudioBookModel(TestBase, TestModelBase):
    
    def setUp(self):
        self._create_audiobook()

    def test_audiobook_object_creation(self):
        audiobook = AudioBook.objects.first()
        self.assertIsNotNone(audiobook)
        self.assertEqual(audiobook.title, self.audiobook_data['title'])
        self.assertEqual(audiobook.narrator, self.audiobook_data['narrator'])
        self.assertEqual(audiobook.author, self.audiobook_data['author'])

