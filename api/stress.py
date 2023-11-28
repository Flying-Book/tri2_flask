from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import time
import json
import requests
import random

stress_api = Blueprint('stress_api', __name__,
                  url_prefix='/api/stress')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(stress_api)

def beautify_json_data(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        beautified_data = []
        for item in data.get('items', []):
            beautified_item = {
                "Q": item.get("Q", ""),
                "id": item.get("id", 0),
                "A1": item.get("A1", ""),
                "A2": item.get("A2", ""),
                "A3": item.get("A3", ""),
                "A4": item.get("A4", ""),
            }

            beautified_data.append(beautified_item)

        return beautified_data  # Return the processed data as a list

    except FileNotFoundError:
        return {"error": "File not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the file"}


beautify_json_data("model/stress.json")


# getJokes()
class _Read(Resource):
    def get(self):
        json_list = []
        json_list.append(beautify_json_data('model/stress.json'))
        return jsonify(json_list)

class _ReadRandom(Resource):
    def get(self):
        beautified_data = beautify_json_data('model/stress.json')
        random_item = random.choice(beautified_data)
        return jsonify(random_item)
    
class _Search(Resource):
    def get(self):
        query = request.args.get('query')  # Get the query parameter
        if not query:
            return {"error": "No query provided"}, 400

        beautified_data = beautify_json_data('model/stress.json')
        results = [item for item in beautified_data if query.lower() in item['name'].lower()]

        return jsonify(results)

class _Count(Resource):
    def get(self):
        beautified_data = beautify_json_data('model/stress.json')
        count = len(beautified_data)
        return {"count": count}

api.add_resource(_Read, '/')
api.add_resource(_ReadRandom, '/random')
api.add_resource(_Search, '/search')
api.add_resource(_Count, '/count')