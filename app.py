import numpy as np
import dash
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import datetime
import re

from constants import *;
from utils import *
from models import *

from server import server;
from dash_layout import *; 
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/',external_stylesheets=[dbc.themes.BOOTSTRAP])

# App gives warning if an imputed value is used in prediction
p1_surface_imputed = False
p2_surface_imputed = False
p1_level_imputed = False
p2_level_imputed = False

app.layout = dash_layout
@app.callback(
	Output('feature', 'options'),
	[Input('surface', 'value'), Input('level', 'value')]
)

def update_radioItems(surface, level):
	'''
	radioItems allow user to select a particular graph to display
	Options are surface win %, head-to-head, level win %, ranking, and recent form
	radioItems options update depending on selected court surface and tournament level
	'''
	options=[{'label': bar_rows_dict[key], 'value': key} for key in bar_rows_dict.keys()]
	for option in options:
		if option['value'] == 'surface_win_pct':
			option['label'] = option['label'] + surface.lower() + ' courts'
		if option['value'] == 'level_win_pct':
			option['label'] = option['label'] + tourney_dict[level] + ' events'
	return options

@app.callback(
	Output('first-player', 'options'),
	Input('second-player', 'value')
)

def update_p1_dropdown(player2):
	'''
	This makes it impossible for the user to select the same player in both dropdown menus.
	Prevents error.
	'''
	updated_player_list = [name for name in player_list if name != player2]
	return [{'label': name, 'value': name} for name in updated_player_list]

@app.callback(
	Output('second-player', 'options'),
	Input('first-player', 'value')
)

def update_p2_dropdown(player1):
	'''
	This makes it impossible for the user to select the same player in both dropdown menus.
	Prevents error.
	'''
	updated_player_list = [name for name in player_list if name != player1]
	return [{'label': name, 'value': name} for name in updated_player_list]

@app.callback(
	Output('prediction', 'children'),
	[Input('first-player', 'value'),
	 Input('second-player', 'value'),
	 Input('surface', 'value'),
	 Input('level', 'value')])

def update_prediction(player1, player2, surface, level):
	'''
	Print the predicted winner of a match between <player1> and <player2>
	on court surface <surface> at tournament at tournament level <level>

	Print the betting odds as predicted by logistic regression model

	Print warning if a value is imputed.
	'''
	
	global p1_surface_imputed, p2_surface_imputed, p1_level_imputed, p2_level_imputed
	p1_surface_imputed = False
	p2_surface_imputed = False
	p1_level_imputed = False
	p2_level_imputed = False
	
	if player2 < player1:
		player1, player2 = player2, player1
	match_series = next_match(player1, player2, surface, level)
	prediction = gbc_best.predict(np.matrix(match_series))
	probability = gbc_best.predict_proba(np.matrix(match_series))
	if prediction == 'player_1':
		pred_statement = 'The predicted winner is ' + player1 + '.'
		p = probability[0,0]
		prob_statement = 'Her odds of winning are ' + str(round(p/(1-p), 2)) + ':1.'
	else:
		pred_statement = 'The predicted winner is ' + player2 + '.'
		p = probability[0,1]
		prob_statement = 'Her odds of winning are ' + str(round(p/(1-p), 2)) + ':1.'
		
	child = [html.H2(pred_statement), html.H3(prob_statement)]
	if p1_surface_imputed:
		child.append(html.H6('Note: No data is available for ' + player1 + ' on ' + surface.lower()
			+ ' courts, so her overall win percent is used in place of her win percent on '
			+ surface.lower() + '.'
		))
	if p2_surface_imputed:
		child.append(html.H6('Note: No data is available for ' + player2 + ' on ' + surface.lower()
			+ ' courts, so her overall win percent is used in place of her win percent on '
			+ surface.lower() + '.'
		))
	if p1_level_imputed:
		child.append(html.H6('Note: No data is available for ' + player1 + ' at ' + tourney_dict[level]
			+ ' events, so her overall win percent is used in place of her win percent at '
			+ tourney_dict[level] + ' events.'
		))
	if p2_level_imputed:
		child.append(html.H6('Note: No data is available for ' + player2 + ' at ' + tourney_dict[level]
			+ ' events, so her overall win percent is used in place of her win percent at '
			+ tourney_dict[level] + ' events.'
		))
	
	return child
	

@app.callback(
	Output('bar-graph', 'figure'),
	[Input('first-player', 'value'),
	 Input('second-player', 'value'),
	 Input('surface', 'value'),
	 Input('level', 'value'),
	 Input('feature', 'value')])

def update_figure(player1, player2, surface, level, feature):
	# print(player1, player2, surface, level, feature)
	'''
	update graph depending on player1, player2, surface, level, and radioItems selection
	y-axis label updates according to set_ylabel function defined earlier
	actual ranking (not log of ranking) is displayed
	'''
	if player2 < player1:
		player1, player2 = player2, player1
	match_series = next_match(player1, player2, surface, level)
	p1_series = match_series[p1_indices]
	p2_series = match_series[p2_indices]
	p1_series.index = bar_rows_dict.keys()
	p2_series.index = bar_rows_dict.keys()
	p1_series['ranking'] = round(np.e**p1_series['ranking'])
	p2_series['ranking'] = round(np.e**p2_series['ranking'])
	
	match_df = pd.DataFrame({'player_1': p1_series, 'player_2': p2_series}).reset_index()
	match_df = pd.melt(match_df, 'index', ['player_1', 'player_2'])
	match_df.columns = match_df.columns.str.replace('variable', 'player')
	match_df.columns = match_df.columns.str.replace('index', 'feature')
	match_df['player'] = match_df['player'].str.replace('player_1', player1)
	match_df['player'] = match_df['player'].str.replace('player_2', player2)
	match_df = match_df.sort_values(by = 'player')
	
	fig = px.bar(
		data_frame = match_df[match_df['feature'] == feature],
		x = 'player',
		y = 'value',
		color = 'player',
		labels = {'player': 'Player\'s Name', 'value': set_ylabel(feature, surface, level)},
		color_discrete_sequence = ['#82AEFF', '#B582FF'],
		width = 800
	)
	
	fig.update_layout(
		transition_duration=500,
		paper_bgcolor='#F9F8FF',
		#plot_bgcolor='#FFFFFF',
		legend={'orientation': 'h', 'yanchor': 'top', 'xanchor': 'right', 'y': 1.1, 'x': 1},
		legend_title_text=None
	)
	
	return fig

if __name__ == '__main__':
	app.run_server(host='0.0.0.0',debug=True, port=8080)