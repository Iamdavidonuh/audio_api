from flask import Flask, request, Response, json, make_response, jsonify
from bson import json_util
from models.db import initialize_db
from models.models import Song, Podcast, AudioBook
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
    audios = Podcast.objects().to_json()
    return Response(audios, mimetype="application/json", status=200)


@app.route('/create', methods=["POST"])
def create_audio():
    a_type = request.json['audioFileType']
    
    if a_type == "song":
        song = Song(
            song_title=request.json['song_title'],
            song_duration=request.json['song_duration']
            )
        song.save()
        response = {
            "id": song.pk,
            "song_title": song.song_title,
            "song_duration": song.song_duration,
            "uploaded": song.uploaded
        }
        return make_response(json.loads(json_util.dumps(response)), 200)
    
    elif a_type == "podcast":
        podcast = Podcast(
            podcast_name=request.json['podcast_name'],
            podcast_duration=request.json['podcast_duration'],
            host=request.json['host'], participants=request.json['participants']
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
        return make_response(json.loads(json_util.dumps(response)), 200)
    elif a_type == "audiobook":
        audiobook = AudioBook(
            title=request.json['title'],
            duration=request.json['duration'],
            author=request.json['author'], narrator=request.json['narrator']
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
        return make_response(json.loads(json_util.dumps(response)), 200)
    else:
        #raise error
        return make_response(jsonify({"error": "Internal Server Error"}), 500)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)