from db import * 
from flask import Flask, request, jsonify, send_file, render_template, make_response
from flask_restful import Resource

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



        return jsonify({'prob': probability[0, 1], 'winner':player2})

class HelloWorld(Resource):

    def get(self):
        num_of_entries = getMatchesCount()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', numOfMatches=num_of_entries, accuracy=0.72),200,headers)

        # return f"<img src='data:image/png;base64,{data}'/>"


class AboutPage(Resource):
    def get(self):

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('about.html', numberOfplayer=getPlayersCount(), fromyear=2018),200,headers)