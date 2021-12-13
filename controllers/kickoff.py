from db import * 
from flask import Flask, request, jsonify, send_file, render_template, make_response
from flask_restful import Resource
seconds_in_year = 365.25 * 24 * 60 * 60

file = open('./data/kickscore.sav', 'rb')

kickscore_model = pickle.load(file)

class KickOff(Resource):

    def get(self):


        p1 = request.args.get('p1')

        p2 = request.args.get('p2')


        if (p2 < p1): p1, p2 = p2, p1

        fig, ax = kickscore_model.plot_scores(

            items=[p1, p2],


            resolution=10/seconds_in_year,


            figsize=(14.0, 3.0),


            timestamps=True)


        ax.set_title("Evolution of skill of 2 tennis players (2000–2021)");


        # Save it to a temporary buffer.


        buf = BytesIO()


        fig.savefig(buf, format="png")


        # Embed the result in the html output.


        data = base64.b64encode(buf.getbuffer()).decode("ascii")


        headers = {'Content-Type': 'text/html'}


        return make_response(f"<img src='data:image/png;base64,{data}'/>",200,headers)

import os.path
# os.path.isfile(fname)
import os
cwd = os.getcwd()
print(cwd)
def saveImageOfTwo(p1, p2):
    if (p1>p2): p1,p2 = p2, p1
    
    newName1 = '-'.join(p1.lower().split(' '))
    newName2 = '-'.join(p2.lower().split(' '))
    fileName = f'/static/versus/{newName1}__{newName2}.png'
    if (os.path.isfile('.' + fileName)):
        return fileName
    
    fig, ax = kickscore_model.plot_scores(

            items=[p1, p2],


            resolution=10/seconds_in_year,


            figsize=(14.0, 3.0),


            timestamps=True)
    ax = f"Evolution of skill of {p1} & {p2}"
    fig.savefig('.' +  fileName)
    return fileName