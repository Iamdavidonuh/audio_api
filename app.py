from flask import Flask, request, Response, json, make_response, jsonify
from flask.views import MethodView
from bson import json_util
from models.db import initialize_db
from models.models import Song, Podcast, AudioBook
from audio_controller import AudioController


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
                response = AudioController.create_song(request.json['song_title'], request.json['song_duration'])
                return make_response(json.loads(json_util.dumps(response)), 200)
            
            elif a_type == "podcast":

                response = AudioController.create_podcasts(
                    podcast_name=request.json['podcast_name'],
                    podcast_duration=request.json['podcast_duration'],
                    host=request.json['host'], participants=request.json['participants']
                    )
                
                return make_response(json.loads(json_util.dumps(response)), 200)
            
            elif a_type == "audiobook":
                response = AudioController.create_audiobooks(
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
                # check if id is None and return all songs
                if id is None:
                    songs = Song.objects.all()
                    return make_response(json.loads(json_util.dumps(songs.to_json())), 200)
                else:
                    response = AudioController.get_song(id)
                    return make_response(json.loads(json_util.dumps(response)), 200)
            
            elif audioFileType == "podcast":
                # get all postcasts if id is None
                if id is None:
                    podcasts = Podcast.objects.all()
                    return make_response(json.loads(json_util.dumps(podcasts.to_json())), 200)
                else:
                    response = AudioController.get_podcast(id)
                    return make_response(json.loads(json_util.dumps(response)), 200)

            elif audioFileType == "audiobook":
                if id is None:
                    audiobooks = AudioBook.objects.all()
                    return make_response(json.loads(json_util.dumps(audiobooks.to_json())), 200)
                else:
                    response = AudioController.get_audiobook(id)
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
                response = AudioController.get_and_update_song(id, body)
                return make_response(json.loads(json_util.dumps(response)), 200)
            
            elif audioFileType == "podcast":
                response = AudioController.get_and_update_podcast(id, body)
                return make_response(json.loads(json_util.dumps(response)), 200)

            elif audioFileType == "audiobook":
                response = AudioController.get_and_update_audiobook(id, body)
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
                response = AudioController.delete_song(id)
                return make_response(response, 200)
            
            elif audioFileType == "podcast":
                response = AudioController.delete_podcast(id)
                return make_response(response, 200)

            elif audioFileType == "audiobook":
                response = AudioController.delete_audiobook(id)
                return make_response(id, 200)
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
    app.run(debug=True)