from models import *
import pandas as pd
import numpy as np
from datetime import datetime
import re
from constants import *
from datetime import date



def next_match(player1, player2, surface, tourney_level):
	# print(player1, player2, surface, tourney_level)
	'''
	this function organizes information for a hypothetical "next match" between two players
	
	Arguments:
	player1: one of the players in the match
	player2: the other player in the match
	surface: surface for the match to be played on
	tourney_level: tournament level where the match will take place

	The various features that go into the logistic regression model are imputed by searching through
	the dataframes matches3 and rankings for the most recent occurences of player1 playing on the
	chosen surface or at the selected tournament level, player1 and player2 playing against each other,
	etc.

	If the data contains no instanes of a player on the surface or tourney_level input, the win %
	is imputed with her overall win %
	'''
	global p1_surface_imputed
	global p2_surface_imputed
	global p1_level_imputed
	global p2_level_imputed
	
	s = pd.Series(dtype = 'float64')
	if player1 < player2:
		p1 = player1
		p2 = player2
	else:
		p1 = player2
		p2 = player1
	
	p1_mask = (matches3['player_1'] == p1) | (matches3['player_2'] == p1)
	p2_mask = (matches3['player_1'] == p2) | (matches3['player_2'] == p2)
	surface_mask = matches3['surface'] == surface
	level_mask = matches3['tourney_level'] == tourney_level
	
	p1_last_match = matches3[p1_mask].iloc[-1]
	p2_last_match = matches3[p2_mask].iloc[-1]
	p1_last_match_surface = matches3[p1_mask & surface_mask]
	p2_last_match_surface = matches3[p2_mask & surface_mask]
	p1_last_match_level = matches3[p1_mask & level_mask]
	p2_last_match_level = matches3[p2_mask & level_mask]
	
	if p1 == p1_last_match['player_1']:
		p1_string = 'player_1_'
	else:
		p1_string = 'player_2_'
		
	if p2 == p2_last_match['player_1']:
		p2_string = 'player_1_'
	else:
		p2_string = 'player_2_'
	
	s['player_1_recent_form'] = p1_last_match[p1_string + 'recent_form']
	s['player_2_recent_form'] = p2_last_match[p2_string + 'recent_form']
	
	p1_id = p1_last_match[p1_string + 'id']
	p1_most_recent_ranking = rankings[rankings['player_id'] == p1_id].iloc[-1]
	s['log_player_1_rank'] = np.log(p1_most_recent_ranking['ranking'])
	
	p2_id = p2_last_match[p2_string + 'id']
	p2_most_recent_ranking = rankings[rankings['player_id'] == p2_id].iloc[-1]
	s['log_player_2_rank'] = np.log(p2_most_recent_ranking['ranking'])
	
	years_ago = (matches3['tourney_date'].apply(lambda x: datetime.utcnow()-x).dt.days/365.2422)
	s['player_1_age'] = p1_last_match[p1_string + 'age'] + years_ago[p1_last_match.name]
	s['player_2_age'] = p2_last_match[p2_string + 'age'] + years_ago[p2_last_match.name]
	

	
	if p1_last_match_surface.shape[0] > 0:
		p1_last_match_surface = p1_last_match_surface.iloc[-1]
		if p1 == p1_last_match_surface['player_1']:
			p1_string = 'player_1_'
		else:
			p1_string = 'player_2_'
		
		s['player_1_surface_win_pct'] = p1_last_match_surface[p1_string + 'surface_win_pct']
	else:
		s['player_1_surface_win_pct'] = p1_last_match[p1_string + 'win_pct']
		p1_surface_imputed = True
		
		
	if p2_last_match_surface.shape[0] > 0:
		p2_last_match_surface = p2_last_match_surface.iloc[-1]
		if p2 == p2_last_match_surface['player_1']:
			p2_string = 'player_1_'
		else:
			p2_string = 'player_2_'
		
		s['player_2_surface_win_pct'] = p2_last_match_surface[p2_string + 'surface_win_pct']
	else:
		s['player_2_surface_win_pct'] = p2_last_match[p2_string + 'win_pct']
		p2_surface_imputed = True
	
	if p1_last_match_level.shape[0] > 0:
		p1_last_match_level = p1_last_match_level.iloc[-1]
		if p1 == p1_last_match_level['player_1']:
			p1_string = 'player_1_'
		else:
			p1_string = 'player_2_'
		
		s['player_1_level_win_pct'] = p1_last_match_level[p1_string + 'level_win_pct']
	else:
		s['player_1_level_win_pct'] = p1_last_match[p1_string + 'win_pct']
		p1_level_imputed = True
		
	if p2_last_match_level.shape[0] > 0:
		p2_last_match_level = p2_last_match_level.iloc[-1]
		if p2 == p2_last_match_level['player_1']:
			p2_string = 'player_1_'
		else:
			p2_string = 'player_2_'
		
		s['player_2_level_win_pct'] = p2_last_match_level[p2_string + 'level_win_pct']
	else:
		s['player_2_level_win_pct'] = p2_last_match[p2_string + 'win_pct']
		p2_level_imputed = True
		

	last_match = matches3[(matches3['player_1'] == p1) & (matches3['player_2'] == p2)]
	if last_match.shape[0] > 0:
		last_match = last_match.iloc[-1]
		s['player_1_h2h'] = last_match['player_1_h2h']
		s['player_2_h2h'] = last_match['player_2_h2h']
	else:
		s['player_1_h2h'] = 0
		s['player_2_h2h'] = 0
	
	for idx in surface_cols:
		if surface in idx:
			s[idx] = 1
		else:
			s[idx] = 0
			
	for idx in level_cols:
		if tourney_level in idx:
			s[idx] = 1
		else:
			s[idx] = 0
	
	s = s[pred_cols]
	return s

# Sets y-axis label for graph in app
def set_ylabel(feature, surface, level):
	if feature == 'recent_form':
		return 'Recent Form'
	if feature == 'surface_win_pct':
		return 'Win Percent on ' + surface
	if feature == 'level_win_pct':
		return 'Win Percent in ' + tourney_dict[level] + ' Matches'
	if feature == 'h2h':
		return 'Head-to-Head Matches Won'
	if feature == 'ranking':
		return 'Player\'s Ranking'


def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj

 
def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

