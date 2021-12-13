from sqlalchemy import create_engine

from utils import * 

from models import *

from constants import * 
engine = create_engine('postgresql://postgres:1622000@localhost/wtatennis')


def getPlayer(id):

    with engine.connect() as conn:

        result = conn.execute(f'select * from players where id={id}')
        if (result.rowcount):
            return dict(result.first())

        return None

def getMatch(id):
    with engine.connect() as conn:
        result = conn.execute(f'select m.*, p1.name as player_1_name, p2.name as player_2_name, p1.photo_url as player_1_photo_url, p2.photo_url as player_2_photo_url  from matches m inner join players p1 on m.player_1_id=p1.id inner join players p2 on m.player_2_id=p2.id where m.id={id}')
        if (result.rowcount):
            dict_row = dict(result.first())
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
            return item
        return None

# print(getPlayer(201527))

def getPlayers(limit=10, offset=0):

    with engine.connect() as conn:

        result = conn.execute(f'select * from players order by id desc limit {limit} offset {offset}')

        # for row in result:

        #     print(dict(row))

        # result = conn.execute(select([users.c.name, users.c.birthday]))

        # for row in result:

        #     print(dict(row))


        return [dict(row) for row in result]

def getPlayersCount():

    with engine.connect() as conn:

        result = conn.execute(f'select count(*) from players')
        for row in result:

            return dict(row)['count']

        # result = conn.execute(select([users.c.name, users.c.birthday]))

        # print(dict(result))


        # return [dict(row) for row in result]

# {'id': 9359, 'player_1_id': 220714, 'player_2_id': 202596, 'player_1_rank': 111, 'player_2_rank': 137, 'player_1_rank_points': 746.0, 'player_2_rank_points': 593, 'tourney_date': datetime.date(2021, 4, 17), 'tourney_level': 'D', 'surface': 'Hard', 'winner_id': 220714, 'tourney_name': 'BJK Cup Playoffs: ROU vs ITA', 'finished': True, 'player_1_name': 'Elisabetta Cocciaretto', 'player_2_name': 'Mihaela Buzarnescu', 'player_1_photo_url': None, 'player_2_photo_url': None}

def getPastMatches(limit=5, offset=0):

       
    with engine.connect() as conn:

        result = conn.execute(f'select m.*, p1.name as player_1_name, p2.name as player_2_name, p1.photo_url as player_1_photo_url, p2.photo_url as player_2_photo_url from matches m inner join players p1 on m.player_1_id=p1.id inner join players p2 on m.player_2_id=p2.id where m.tourney_date < CURRENT_DATE order by m.id desc limit {limit} offset {offset}')
        res = []
        for row in result:
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
            res.append(item)
        return res 

def getUpcomingMatches(limit=5, offset=0):
    with engine.connect() as conn:
        result = conn.execute(f'select m.*, p1.name as player_1_name, p2.name as player_2_name, p1.photo_url as player_1_photo_url, p2.photo_url as player_2_photo_url from matches m inner join players p1 on m.player_1_id=p1.id inner join players p2 on m.player_2_id=p2.id where m.tourney_date > CURRENT_DATE order by m.tourney_date asc limit {limit} offset {offset}')
        res = []
        for row in result:
            dict_row = dict(row)
            item = {}
            player1 = dict_row['player_1_name']
            player2 = dict_row['player_2_name']
            surface = dict_row['surface']
            level = dict_row['tourney_level']
            # continue

            # break

            # match_series = next_match(player1, player2, surface, level)

            # prediction = gbc_best.predict(np.matrix(match_series))

            # probability = gbc_best.predict_proba(np.matrix(match_series))

            # prob = 0

            # if prediction == 'player_1':

            #     prob = probability[0, 0]

            # else:

            #     prob = probability[0, 1]

            item['id'] = dict_row['id']

            item['player1'] = {'name': player1, 'photo_url': dict_row['player_1_photo_url'], 'prob': dict_row['player_1_prob']}

            item['player2'] = {'name': player2, 'photo_url': dict_row['player_2_photo_url'], 'prob': dict_row['player_2_prob']}

            item['date'] = dict_row['tourney_date']

            item['surface'] = dict_row['surface']

            item['tourney_name'] = dict_row['tourney_name']

            item['tourney_level'] = level
            res.append(item)
        return res 

def getMatchesCount():

    with engine.connect() as conn:

        result = conn.execute(f'select count(*) from matches')
        for row in result:

            return dict(row)['count']

        # result = conn.execute(select([users.c.name, users.c.birthday]))

        # print(dict(result))


        # return [dict(row) for row in result]