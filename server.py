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
from controllers.predict import *

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from db import maskAsFinished;

scheduler = BackgroundScheduler()
scheduler.add_job(func=maskAsFinished, trigger="interval", days=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


server = Flask(__name__)


api = Api(server, catch_all_404s=True)


CORS(server)


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

