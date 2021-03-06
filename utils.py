from models.models import Song, Podcast, AudioBook


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

def create_podcasts(**kwargs):
    """
    Creates a Podcasts object and save's it to the database
    :type response dict
    :return response
    """
    podcast = Podcast(
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