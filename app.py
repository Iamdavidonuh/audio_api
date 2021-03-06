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
    audios = Podcast.objects().to_json()
    return Response(audios, mimetype="application/json", status=200)

class CreateAudiosView(MethodView):
    def post(self):
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
            return make_response(jsonify({"error": "Internal Server Error"}), 500)




app.add_url_rule('/audio/create/', view_func=CreateAudiosView.as_view('create_audio_song_podcast_audiobook'))

# Run Server
if __name__ == "__main__":
    app.run(debug=True)