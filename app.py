from flask import Flask, request, Response, json, make_response, jsonify
from flask.views import MethodView
from bson import json_util
from models.db import initialize_db
from models.models import Song, Podcast, AudioBook
from utils import create_song, create_podcasts, create_audiobooks
#init app
app = Flask(__name__)

# db
app.config['MONGODB_DB'] = 'admin'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017
app.config['MONGODB_USERNAME'] = 'admin'
app.config['MONGODB_PASSWORD'] = 'password'
initialize_db(app)


@app.route('/', methods=['GET'])
def get_audios():
    audios = Song.objects().to_json()
    podcasts = Podcast.objects.to_json()
    audiobook = AudioBook.objects.to_json()
    return Response(audios, mimetype="application/json", status=200)

#Post requests
class CreateAudiosView(MethodView):
    """
    Used to create 3 types of audio file: songs, podcasts, audiobooks
    """
    def post(self):

        try:
            a_type = request.json['audioFileType']
        
            if a_type == "song":
                response = create_song(request.json['song_title'], request.json['song_duration'])
                return make_response(json.loads(json_util.dumps(response)), 200)
            
            elif a_type == "podcast":

                response = create_podcasts(
                    podcast_name=request.json['podcast_name'],
                    podcast_duration=request.json['podcast_duration'],
                    host=request.json['host'], participants=request.json['participants']
                    )
                
                return make_response(json.loads(json_util.dumps(response)), 200)
            
            elif a_type == "audiobook":
                response = create_audiobooks(
                    title=request.json['title'],
                    duration=request.json['duration'],
                    author=request.json['author'], narrator=request.json['narrator']
                )
                return make_response(json.loads(json_util.dumps(response)), 200)
            else:
                #raise error
                return make_response(jsonify({"error": "Bad Request"}), 400)
        except Exception():
            return make_response(jsonify({"error": "Internal Server Error"}), 500)

# Get Requests
class GetAudioView(MethodView):
    """
    Returns an audio(podcast, song or audiobook) based on audioFileType and id
    """
    def get(self, audioFileType, id):
        try:
            if audioFileType == "song":
                song = Song.objects.get_or_404(id=id)
                
                response = {
                    "id": song.pk,
                    "song_title": song.song_title,
                    "song_duration": song.song_duration,
                    "uploaded": song.uploaded
                }
                return make_response(json.loads(json_util.dumps(response)), 200)
            
            elif audioFileType == "podcast":
                podcast = Podcast.objects.get_or_404(id=id)
                response = {
                    "id": podcast.pk,
                    "podcast_name": podcast.podcast_name,
                    "podcast_duration": podcast.podcast_duration,
                    "host": podcast.host,
                    "participants": podcast.participants,
                    "uploaded": podcast.uploaded
                }
                return make_response(json.loads(json_util.dumps(response)), 200)

            elif audioFileType == "audiobook":
                audiobook = AudioBook.objects.get(id=id)
                response = {
                    "id": audiobook.pk,
                    "title": audiobook.title,
                    "duration": audiobook.duration,
                    "author": audiobook.author,
                    "narrator": audiobook.narrator,
                    "uploaded": audiobook.uploaded
                }
                return make_response(json.loads(json_util.dumps(response)), 200)
            else:
                return make_response(jsonify({"error": "Bad Request"}), 400)
        except Exception():
            return make_response(jsonify({"error": "Internal Server Error"}), 500)


class UpdateAudioView(MethodView):
    """
    Updates and returns an audio(podcast, song or audiobook)
    based on audioFileType and id
    """

    def put(self, audioFileType, id):
        try:
            body = request.get_json()
            body.pop("audioFileType")
            if audioFileType == "song":
                Song.objects.get_or_404(id=id).update(**body)
                song = Song.objects.get_or_404(id=id)
                response = {
                    "id": song.pk,
                    "song_title": song.song_title,
                    "song_duration": song.song_duration,
                    "uploaded": song.uploaded
                }
                return make_response(json.loads(json_util.dumps(response)), 200)
            
            elif audioFileType == "podcast":
                Podcast.objects.get_or_404(id=id).update(**body)
                podcast = Podcast.objects.get_or_404(id=id)
                response = {
                    "id": podcast.pk,
                    "podcast_name": podcast.podcast_name,
                    "podcast_duration": podcast.podcast_duration,
                    "host": podcast.host,
                    "participants": podcast.participants,
                    "uploaded": podcast.uploaded
                }
                return make_response(json.loads(json_util.dumps(response)), 200)

            elif audioFileType == "audiobook":
                AudioBook.objects.get_or_404(id=id).update(**body)
                audiobook = AudioBook.objects.get(id=id)
                response = {
                    "id": audiobook.pk,
                    "title": audiobook.title,
                    "duration": audiobook.duration,
                    "author": audiobook.author,
                    "narrator": audiobook.narrator,
                    "uploaded": audiobook.uploaded
                }
                return make_response(json.loads(json_util.dumps(response)), 200)
            else:
                return make_response(jsonify({"error": "Bad Request"}), 400)
        except Exception():
            return make_response(jsonify({"error": "Internal Server Error"}), 500)


class DeleteAudioView(MethodView):
    """
    Deletes an audio(podcast, song or audiobook)
    based on audioFileType and id
    """

    def delete(self, audioFileType, id):
        try:
            if audioFileType == "song":
                Song.objects.get_or_404(id=id).delete()

                return make_response({}, 200)
            
            elif audioFileType == "podcast":
                Podcast.objects.get_or_404(id=id).delete()
                return make_response({}, 200)

            elif audioFileType == "audiobook":
                AudioBook.objects.get_or_404(id=id).delete()
                return make_response({}, 200)
            else:
                return make_response(jsonify({"error": "Bad Request"}), 400)
        except Exception():
            return make_response(jsonify({"error": "Internal Server Error"}), 500)


# create
app.add_url_rule('/create/', view_func=CreateAudiosView.as_view('create_audio_song_podcast_audiobook'))

# get
app.add_url_rule(
    '/get/<audioFileType>/<id>',
    view_func=GetAudioView.as_view("get_audio_song_podcast_audiobook"),
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
    app.run(debug=True)