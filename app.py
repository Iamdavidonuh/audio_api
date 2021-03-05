from flask import Flask, request, jsonify, Response
from models.db import initialize_db
from models.models import Song, Podcast, AudioBook
import os


#init app
app = Flask(__name__)

# db
app.config['MONGODB_DB'] = 'admin'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017
app.config['MONGODB_USERNAME'] = 'admin'
app.config['MONGODB_PASSWORD'] = 'password'
initialize_db(app)


@app.route('/')
def get_audios():
    audios = Song.objects().to_json()
    return Response(audios, mimetype="application/json", status=200)

# Run Server
if __name__ == "__main__":
    app.run(debug=True)