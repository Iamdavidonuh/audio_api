from flask import Flask, request, Response, json, make_response, jsonify
from src.models.db import initialize_db
from src.models.models import Song, Podcast, AudioBook
from src.audio_controller import AudioController
from src.views import CreateAudiosView, GetAudioView, UpdateAudioView, DeleteAudioView


#init app
app = Flask(__name__)

# db
app.config['MONGODB_SETTINGS'] = {
    'db': 'test_db',
    'host': 'localhost',
    'port': 27017,
    'username': 'admin',
    'password': 'password',
    'authentication_source': 'admin'}


@app.route('/', methods=['GET'])
def get_audios():
    audios = Song.objects().to_json()
    podcasts = Podcast.objects.to_json()
    audiobook = AudioBook.objects.to_json()
    return Response(audios, mimetype="application/json", status=200)




# create
app.add_url_rule('/create/', view_func=CreateAudiosView.as_view('create_audio_song_podcast_audiobook'))

# get
app.add_url_rule(
    '/get/<audioFileType>/<id>',
    view_func=GetAudioView.as_view("get_audio_song_podcast_audiobook"),
    methods=["GET",]
    )
app.add_url_rule(
    '/get/<audioFileType>/', defaults={'id': None},
    view_func=GetAudioView.as_view("get_all_song_podcast_audiobook"),
    methods=["GET",]
    )

# update
app.add_url_rule(
    '/update/<audioFileType>/<id>',
    view_func=UpdateAudioView.as_view("update_audio_song_podcast_audiobook"),
    methods=["PUT",]
    )

# delete
app.add_url_rule(
    '/delete/<audioFileType>/<id>',
    view_func=DeleteAudioView.as_view("delete_audio_song_podcast_audiobook"),
    methods=["DELETE",]
    )


# Run Server
if __name__ == "__main__":
    initialize_db(app)
    app.run(debug=True)