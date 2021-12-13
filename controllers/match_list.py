from db import * 
from flask import Flask, request, jsonify, send_file, render_template, make_response
from flask_restful import Resource

class MatchList(Resource):
    def get(self):

        page = int(request.args.get('page', 0))

        pageSize = int(request.args.get('pageSize', 10))

        offset = page*pageSize

        num_of_entries = getMatchesCount()

        num_of_page = num_of_entries // pageSize + 1

        return jsonify({'content' : getPastMatches(pageSize, offset), 'page' : page, 'pageSize': pageSize, 'numOfEntries' : num_of_entries, 'numOfPage': num_of_page})

    def post(self):
        body = request.get_json()
        if (createMatch(body)):
            return jsonify({'content' : body, 'message': 'Success'})

        return jsonify({'content' : body, 'message': 'FAIL'}), 400


class Matches(Resource):

    def get(self, match_id):

        match = getMatch(match_id)

        if (not match): abort(404,  message='match not found')
        return jsonify({'content' : match})


class MatchesPage(Resource):

    def get(self):

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('matches.html'),200,headers)

class MatchPage(Resource):

    def get(self, match_id):
        match = getMatch(match_id)
        if (not match): abort(404,  message='match not found')
        
        headers = {'Content-Type': 'text/html'}
        
        return make_response(render_template('match.html', player1=match['player1'], player2=match['player2'],
        date=match['date'], surface=match['surface'], tourney_name=match['tourney_name'], tourney_level=match['tourney_level']
        , kickscore=match['kickscore']),200,headers)