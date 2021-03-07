from mongoengine.errors import DoesNotExist
from tests.test_base import TestBase, TestModelBase

from src.models.models import Song, AudioBook, Podcast
from src.audio_controller import AudioController


class TestAudioController(TestBase, TestModelBase):

    def setUp(self):
        super().setUp()

        self._create_song()
        self.song_id = Song.objects.first().id
        self._create_podcast()
        self.podcast_id = Podcast.objects.first().id

        self._create_audiobook()
        self.audiobook_id = AudioBook.objects.first().id
    
    # Create
    def test_create_song(self):
        response = AudioController.create_song(self.song_data["song_title"], self.song_data["song_duration"])
        song = Song.objects.first()
        self.assertIsNotNone(Song)
        self.assertEqual(response["song_title"], song.song_title)
        self.assertTrue(type(response), dict)

    def test_create_podcast(self):
        response = AudioController.create_podcasts(**self.podcast_data)
        podcast = Podcast.objects.first()
        self.assertIsNotNone(podcast)
        self.assertEqual(response["podcast_name"], podcast.podcast_name)
        self.assertTrue(type(response), dict)

    def test_create_podcast(self):
        response = AudioController.create_audiobooks(**self.audiobook_data)
        audiobook = AudioBook.objects.first()
        self.assertIsNotNone(audiobook)
        self.assertEqual(response["title"], audiobook.title)
        self.assertTrue(type(response), dict)

    # Get
    def test_get_song(self):
        response = AudioController.get_song(self.song_id)
        self.assertIsNotNone(response)
        self.assertEqual(type(response), dict)

    def test_get_podcast(self):
        response = AudioController.get_podcast(self.podcast_id)
        self.assertIsNotNone(response)
        self.assertEqual(type(response), dict)

    def test_get_audiobook(self):
        response = AudioController.get_audiobook(self.audiobook_id)
        self.assertIsNotNone(response)
        self.assertEqual(type(response), dict)


    # Delete
    def test_delete_song(self):
        response = AudioController.delete_song(self.song_id)
        self.assertEqual(response, {})
        with self.assertRaises(DoesNotExist):
            query = Song.objects.get(id=self.song_id)
            self.assertIsNone(query)

    def test_delete_podcast(self):
        response = AudioController.delete_podcast(self.podcast_id)
        self.assertEqual(response, {})
        with self.assertRaises(DoesNotExist):
            query = Podcast.objects.get(id=self.podcast_id)
            self.assertIsNone(query)

    def test_delete_audiobook(self):
        response = AudioController.delete_audiobook(self.audiobook_id)
        self.assertEqual(response, {})
        with self.assertRaises(DoesNotExist):
            query = AudioBook.objects.get(id=self.audiobook_id)
            self.assertIsNone(query)
    

    # Update

    def test_update_song(self):
        data = self.song_data.copy()
        data["song_title"] = "Updated " + data['song_title'] 
        response = AudioController.get_and_update_song(self.song_id, data)


        self.assertIn("Updated", response["song_title"])
        self.assertEqual(data["song_title"], response["song_title"])


    def test_update_podcast(self):
        data = self.podcast_data.copy()
        data["host"] = "Test1"
        data["podcast_name"] = "Updated " + data['podcast_name'] 
        response = AudioController.get_and_update_podcast(self.podcast_id, data)

        self.assertIn("Updated", response["podcast_name"])
        self.assertEqual(data["podcast_name"], response["podcast_name"])
        self.assertTrue(response["host"], "Test1")


    def test_update_audiobook(self):
        data = self.audiobook_data.copy()
        data["title"] = "Updated " + data['title']
        data["author"] = "Test"
        response = AudioController.get_and_update_audiobook(self.audiobook_id, data)

        self.assertIn("Updated", response["title"])
        self.assertTrue(response["author"], "Test")