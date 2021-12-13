from db import * 
from flask import Flask, request, jsonify, send_file, render_template, make_response
from flask_restful import Resource

class PlayerList(Resource):
    def get(self):
        page = int(request.args.get('page', 0))
        pageSize = int(request.args.get('pageSize', 10))
        offset = page*pageSize
        num_of_entries = getPlayersCount()
        num_of_page = num_of_entries // pageSize + 1
        return jsonify({'content' : getPlayers(pageSize, offset), 'page' : page, 'pageSize': pageSize, 'numOfEntries' : num_of_entries, 'numOfPage': num_of_page})
    def post(self):
        pass