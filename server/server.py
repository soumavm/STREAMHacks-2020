#!/usr/bin/env python

import os

from dotenv import load_dotenv
load_dotenv()

import flask
from flask import request, jsonify
app = flask.Flask(__name__)
app.config['DEBUG'] = True

import flask_cors
from flask_cors import CORS
CORS(app)

apiKey = os.getenv("APIKEY")

geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json?key=" + apiKey
searchURL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=" + apiKey
photoURL = "https://maps.googleapis.com/maps/api/place/photo?key=" + apiKey

def listNearby(location, request):
    payload = {
        'location': location,
        'rankby': 'distance'
    }

    if 'type' in request.args:
        payload['keyword'] = request.args.get('type')

    listPlaces = requests.get(searchURL, params=payload).json()

    return listPlaces['results']

@app.route('/', methods=['GET'])
def home():
    return "Hello, world!"

@app.route('/api/coordinates', methods=['GET'])
def api_coordinates():
    results = []
    status = 'Success'
    statusCode = 200

    if 'lat' in request.args and 'lng' in request.args:
        latitude = request.args.get('lat')
        longitude = request.args.get('lng')

        location = latitude + ',' + longitude

        results = listNearby(location, request)

        app.logger.info("Received coordinates request for %s,%s and returned %s results with status %s (%s)", latitude, longitude, len(results), statusCode, status)

    else:
        status = 'Invalid request'
        statusCode = 400

        app.logger.info("Received invalid coordinates request and returned %s results with status %s (%s)", len(results), statusCode, status)

    response = {
        'results': results,
        'status': status
    }

    return jsonify(response), statusCode

app.run()

