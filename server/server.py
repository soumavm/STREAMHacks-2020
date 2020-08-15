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

import requests

apiKey = os.getenv("APIKEY")

geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json?key=" + apiKey
searchURL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=" + apiKey

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

def geocoding(address):
    payload = {
        'address': address
    }

    geocoded = requests.get(geocodeURL, params=payload)

    geocodedLocation = geocoded.json()['results'][0]['geometry']['location']

    latitude = geocodedLocation['lat']
    longitude = geocodedLocation['lng']

    return str(latitude) + ',' + str(longitude)

@app.route('/api/address', methods=['GET'])
def api_address():
    results = []
    status = 'Success'
    statusCode = 200

    if 'address' in request.args:
        address = request.args.get('address')

        location = geocoding(address)

        results = listNearby(location, request)

        app.logger.info("Received address request for %s and returned %s results with status %s (%s)", address, len(results), statusCode, status)

    else:
        app.logger.info("Received invalid address request and returned %s results with status %s (%s)", len(results), statusCode, status)
        status = 'Invalid request'
        statusCode = 400

    response = {
        'results': results,
        'status': status,
    }

    return jsonify(response), statusCode

app.run()

