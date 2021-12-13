from flask import Flask, request, jsonify, send_file, render_template, make_response


from flask_restful import reqparse, abort, Api, Resource



from io import StringIO
import numpy as np


from skimage.io import imsave

import matplotlib.pyplot as plt


import base64


from io import BytesIO


from matplotlib.figure import Figure


from models import * 


from utils import * 


from db import * 

from flask_cors import CORS

from controllers.match_list import *
from controllers.past_match import *
from controllers.player_list import *
from controllers.upcoming_match import *
from controllers.kickoff import *

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from db import maskAsFinished;

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", days=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


server = Flask(__name__)


api = Api(server, catch_all_404s=True)


CORS(server)



file = open('./data/kickscore.sav', 'rb')

kickscore_model = pickle.load(file)



class HelloWorld(Resource):

    def get(self):
        num_of_entries = getMatchesCount()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', numOfMatches=num_of_entries, accuracy=0.72),200,headers)

        # return f"<img src='data:image/png;base64,{data}'/>"

class Predict(Resource):

    def get(self):


        return {'predict': 'world'}

    def post(self):


        body = request.get_json()


        player1 = body['player1']


        player2 = body['player2']


        surface = body['surface']


        level = body['level']


        if player2 < player1: player1, player2 = player2, player1


        match_series = next_match(player1, player2, surface, level)


        prediction = gbc_best.predict(np.matrix(match_series))


        probability = gbc_best.predict_proba(np.matrix(match_series))


        if prediction == 'player_1':


            return {'prob': probability[0, 0], 'pred': player1}



        return {'prob': probability[0, 1], 'winner':player2}


class Players(Resource):
    def get(self, player_id):

        player = getPlayer(player_id)

        if (not player): abort(404, message='player not found')

        return jsonify({'content' : player})



class MatchPage(Resource):

    def get(self, match_id):
        match = getMatch(match_id)
        if (not match): abort(404,  message='match not found')
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('match.html', player1=match['player1'], player2=match['player2'],
        date=match['date'], surface=match['surface'], tourney_name=match['tourney_name'], tourney_level=match['tourney_level']
        ),200,headers)
        

class PlayerPage(Resource):
    def get(self, player_id):

        player = getPlayer(player_id)

        if (not player): abort(404, message='player not found')

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('player.html', player=player),200,headers)

class MatchesPage(Resource):

    def get(self):

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('matches.html'),200,headers)
        

class PlayersPage(Resource):
    def get(self):

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('players.html'),200,headers)
        
class AboutPage(Resource):
    def get(self):

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('about.html'),200,headers)




class Matches(Resource):

    def get(self, match_id):

        match = getMatch(match_id)

        if (not match): abort(404,  message='match not found')
        return jsonify({'content' : match})
        
        

api.add_resource(HelloWorld, '/')
api.add_resource(AboutPage, '/about')
api.add_resource(PlayersPage, '/players')
api.add_resource(MatchesPage, '/matches')
api.add_resource(MatchPage, '/match/<match_id>')
api.add_resource(PlayerPage, '/player/<player_id>')

api.add_resource(Predict, '/api/predict')

api.add_resource(KickOff, '/api/kickoff')

api.add_resource(Players, '/api/players/<player_id>')

api.add_resource(Matches, '/api/matches/<match_id>')

api.add_resource(MatchList, '/api/matches')

api.add_resource(PlayerList, '/api/players')

api.add_resource(UpcomingList, '/api/upcoming')

api.add_resource(PastResultList, '/api/pastresult')

