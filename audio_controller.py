from models.models import Song, Podcast, AudioBook

class AudioController():

    @staticmethod
    def create_song(song_title, song_duration):
        """
        Creates a Song object and save's it to the database
        :type response dict
        :return response
        """
        song = Song(song_title=song_title, song_duration=song_duration)
        song.save()
        response = {
                "id": song.pk,
                "song_title": song.song_title,
                "song_duration": song.song_duration,
                "uploaded": song.uploaded
            }
        return response

    @staticmethod
    def create_podcasts(**kwargs):
        """
        Creates a Podcasts object and save's it to the database
        :type response dict
        :return response
        """
        podcast = Podcast(self, 
                podcast_name=kwargs['podcast_name'],
                podcast_duration=kwargs['podcast_duration'],
                host=kwargs['host'], participants=kwargs['participants']
                )
        podcast.save()

        response = {
            "id": podcast.pk,
            "podcast_name": podcast.podcast_name,
            "podcast_duration": podcast.podcast_duration,
            "host": podcast.host,
            "participants": podcast.participants,
            "uploaded": podcast.uploaded
        }
        return response

    @staticmethod
    def create_audiobooks(**kwargs):
        """
        Creates a AudioBook object and save's it to the database
        :type response dict
        :return response
        """
        audiobook = AudioBook(
            title=kwargs['title'], duration=kwargs['duration'],
            author=kwargs['author'], narrator=kwargs['narrator']
        )
        audiobook.save()

        response = {
            "id": audiobook.pk,
            "title": audiobook.title,
            "duration": audiobook.duration,
            "author": audiobook.author,
            "narrator": audiobook.narrator,
            "uploaded": audiobook.uploaded
        }
        return response
    
    @staticmethod
    def get_song(id):
        """ Returns a song from the database by the id"""
        song = Song.objects.get_or_404(id=id)
                    
        response = {
            "id": song.pk,
            "song_title": song.song_title,
            "song_duration": song.song_duration,
            "uploaded": song.uploaded
        }
        return response

    @staticmethod
    def get_podcast(id):
        """ Returns a podcast from the database by the id"""
        podcast = Podcast.objects.get_or_404(id=id)
        response = {
            "id": podcast.pk,
            "podcast_name": podcast.podcast_name,
            "podcast_duration": podcast.podcast_duration,
            "host": podcast.host,
            "participants": podcast.participants,
            "uploaded": podcast.uploaded
        }
        return response

    @staticmethod
    def get_audiobook(id):
        """ Returns a podcast from the database by the id"""
        audiobook = AudioBook.objects.get(id=id)
        response = {
            "id": audiobook.pk,
            "title": audiobook.title,
            "duration": audiobook.duration,
            "author": audiobook.author,
            "narrator": audiobook.narrator,
            "uploaded": audiobook.uploaded
        }
        return response