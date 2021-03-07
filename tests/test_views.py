from flask import json
from unittest.mock import patch
from src.models.models import Song
from .test_base import TestBase, TestModelBase

class TestCreateView(TestBase, TestModelBase):
    
    def test_createview_with_song(self):
        song_data = self.song_data.copy()
        song_data['audioFileType'] = 'song'
        payload = json.dumps(song_data)

        response = self.app.post('/create/', headers={"Content-Type": "application/json"}, data=payload)
        
        self.assertEqual(song_data['song_title'], response.json["song_title"])
        self.assertEqual(response.status_code, 200)


    def test_createview_with_podcasts(self):
        
        podcast_data = self.podcast_data.copy()
        
        podcast_data['audioFileType'] = 'podcast'
        payload = json.dumps(podcast_data)
        response = self.app.post('/create/', headers={"Content-Type": "application/json"}, data=payload)
        
        self.assertEqual(podcast_data['podcast_name'], response.json["podcast_name"])
        self.assertEqual(response.status_code, 200)

    def test_createview_with_audiobook(self):
        audiobook_data = self.audiobook_data.copy()
        audiobook_data['audioFileType'] = 'audiobook'
        payload = json.dumps(audiobook_data)
        response = self.app.post('/create/', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(audiobook_data['title'], response.json["title"])
        self.assertEqual(response.status_code, 200)
    

