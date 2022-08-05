from sqlalchemy import create_engine

from utils import * 

from models import *

from constants import * 
from controllers.kickoff import *
import os

DATABASE_URL = os.environ['DATABASE_URL']

# DATABASE_URL = 'postgresql://postgres:1622000@localhost/wtatennis'
# DATABASE_URL = 'postgresql://oihmxqwkduigll:073c3d5640b4a5eabb6ff895a4738f6d82c59951f65a6f57ee17de5589f05cdb@ec2-44-195-100-240.compute-1.amazonaws.com:5432/dbc99k61r8kms4'
engine = create_engine(DATABASE_URL)


def getPlayerByName(id):

    with engine.connect() as conn:

        result = conn.execute(f"select * from players where name='{id}'")
        if (result.rowcount):
            res =  dict(result.first())
            res['age'] = age(res['dob'])
            res['rank'] = 1
            return res
        return None
def getPlayer(id):

    with engine.connect() as conn:

        result = conn.execute(f'select p.*, r.rank, r.points from players p inner join ranks r on p.id = r.player_id where p.id={id} order by ranking_date desc')
        if (result.rowcount):
            res =  dict(result.first())
            res['age'] = age(res['dob'])
            playername = '-'.join(res['name'].lower().split(' '))
            res['kickscore'] = f"/static/playerscore/{playername}.png"
            # res['rank'] = res(['rank'])
            # res['points'] = res(['points'])
            return res
        return None

def getMatch(id):
    with engine.connect() as conn:
        result = conn.execute(f'select m.*, p1.name as player_1_name, p2.name as player_2_name, p1.photo_url as player_1_photo_url, p2.photo_url as player_2_photo_url  from matches m inner join players p1 on m.player_1_id=p1.id inner join players p2 on m.player_2_id=p2.id where m.id={id}')
        if (result.rowcount):
            row = dict(result.first())
           
            return convertMatch(row)
        return None

# print(getPlayer(201527))

def getPlayers(limit=10, offset=0):

    with engine.connect() as conn:

        result = conn.execute(f'select * from players where dob is not null and photo_url is not null order by id desc limit {limit} offset {offset}')
        res = []
        for row in result:

            row_dict =  dict(row)
            row_dict['age'] = age(row_dict['dob'])
            row_dict['rank'] = 1
            playername = '-'.join(row_dict['name'].lower().split(' '))
            row_dict['kickscore'] = f"/static/playerscore/{playername}.png"
            res.append(row_dict)
        return res;
       
def getPlayersCount():

    with engine.connect() as conn:

        result = conn.execute(f'select count(*) from players')
        for row in result:

            return dict(row)['count']

def getPastMatches(limit=5, offset=0):

    with engine.connect() as conn:

        result = conn.execute(f'select m.*, p1.name as player_1_name, p2.name as player_2_name, p1.photo_url as player_1_photo_url, p2.photo_url as player_2_photo_url from matches m inner join players p1 on m.player_1_id=p1.id inner join players p2 on m.player_2_id=p2.id where m.tourney_date < CURRENT_DATE order by m.id desc limit {limit} offset {offset}')
        res = []
        for row in result:
            res.append(convertMatch(row))
        return res 

def getUpcomingMatches(limit=5, offset=0):
    with engine.connect() as conn:
        result = conn.execute(f'select m.*, p1.name as player_1_name, p2.name as player_2_name, p1.photo_url as player_1_photo_url, p2.photo_url as player_2_photo_url from matches m inner join players p1 on m.player_1_id=p1.id inner join players p2 on m.player_2_id=p2.id where m.tourney_date > CURRENT_DATE order by m.tourney_date asc limit {limit} offset {offset}')
        res = []
        for row in result:
            
            res.append(convertMatch(row))
        return res 

def getMatchesCount():

    with engine.connect() as conn:
        result = conn.execute(f'select count(*) from matches')
        for row in result:

            return dict(row)['count']

def createMatch(data):
    player_1_name = data['player1']
    player_2_name = data['player2']
    surface = data['surface']
    tourney_date = data['date']
    tourney_name = data['name']
    tourney_level = data['level']
    finished = data['finished']
    player1 = getPlayerByName(player_1_name)
    player2 = getPlayerByName(player_2_name)
    if (not player1 or not player2): return None

    player_1_id = player1['id']
    player_2_id = player2['id']
    
    match_series = next_match(player_1_name, player_2_name, surface, tourney_level)

    prediction = gbc_best.predict(np.matrix(match_series))

    probability = gbc_best.predict_proba(np.matrix(match_series))

    player_1_prob = probability[0, 0]

    player_2_prob = probability[0, 1]
    with engine.connect() as conn:

        result = conn.execute(f'insert into matches(player_1_id,player_2_id,player_1_prob, player_2_prob ,surface, tourney_date, tourney_level, finished, tourney_name) '
        + f"values({player_1_id}, {player_2_id}, {player_1_prob}, {player_2_prob},'{surface}', '{tourney_date}', '{tourney_level}', {finished}, '{tourney_name}')"
        )
    return True

def maskAsFinished():
    with engine.connect() as conn:

        result = conn.execute(f"update matches set finished=TRUE where tourney_date < CURRENT_DATE")
    return True

def convertMatch(row):
    dict_row = dict(row)
    item = {}
    player1 = dict_row['player_1_name']
    player2 = dict_row['player_2_name']
    surface = dict_row['surface']
    level = dict_row['tourney_level']

    item['id'] = dict_row['id']

    item['player1'] = {'id' : dict_row['player_1_id'], 'name': player1, 'photo_url': dict_row['player_1_photo_url'], 'prob': dict_row['player_1_prob']}

    item['player2'] = {'id' : dict_row['player_2_id'],'name': player2, 'photo_url': dict_row['player_2_photo_url'], 'prob': dict_row['player_2_prob']}

    item['date'] = dict_row['tourney_date']

    item['surface'] = dict_row['surface']

    item['tourney_name'] = dict_row['tourney_name']

    item['tourney_level'] = tourney_dict[level]
    item['winner_id'] = dict_row['winner_id']
    item['kickscore'] = saveImageOfTwo(player1, player2)
    return item
