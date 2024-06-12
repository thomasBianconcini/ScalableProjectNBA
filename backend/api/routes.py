from flask import json, request, jsonify
from flask_restx import Resource, fields, Namespace
from nba_api.stats.endpoints import leaguegamefinder
from datetime import datetime

from api.predict import predict

api = Namespace('api', description='Test API')

api_key = api.model('API Key', {
    'key': fields.String(required=True, description='Chiave API')
})

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

allowed_api_keys = ['taylor']

def check_api_key(key):
    return key in allowed_api_keys

@api.route('/scoreboard')
class ScoreBoard(Resource):
    def get(self):
        team_id = 1610612747  # ID dei Los Angeles Lakers
        game_finder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
        games = game_finder.get_data_frames()[0]

        # Visualizza lo schedule
        print(games)
        return jsonify(games)

@api.route("/predict")
class HelloWorld(Resource):
    @api.doc(security='apikey')
    @api.expect(api_key)
    def get(self):
         print(request.headers)
         api_key = request.headers.get('X-API-KEY')
         if not check_api_key(api_key):
           return {'message': 'Chiave API non valida'}, 401
         
         squadra1 = request.args.get('squadra1')
         squadra2 = request.args.get('squadra2')

         return predict(squadra1,squadra2)
         
