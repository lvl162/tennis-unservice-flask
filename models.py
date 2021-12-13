import pandas as pd


from sklearn.linear_model import LogisticRegression


import pickle



X_train = pd.read_pickle('./data/X_train.data') #the (dummified) feature space used in logistic regression model


# y_train = pd.read_pickle('./y_train.data') #target variable


matches3 = pd.read_pickle('./data/matches3.data') #original data set (post-feature engineering), with all features and all rows


rankings = pd.read_pickle('./data/rankings.data') #complete player rankings


gbc_best = pickle.load(open('./data/gbc_model.sav', 'rb'))




# convert tournament dates to datetime


matches3['tourney_date'] = pd.to_datetime(matches3['tourney_date'], format = '%Y-%m-%d')






# best logistic regression model obtained from grid search in capstone_final Jupyter Notebook


# log_best = LogisticRegression(C=7.585775750291836, solver='liblinear')


# log_best.fit(X_train_log, y_train)






pred_cols = X_train.columns #features in ML model ***in correct order***






#Column names for dummy variables


level_cols = list(filter(lambda c: 'tourney_level' in c, X_train.columns))


surface_cols = list(filter(lambda c: 'surface' in c and 'win' not in c, X_train.columns))











# IDs of players to include in app dropdown menus.


# Only want to include players who have played in the last 2 seasons


current_ids = rankings[rankings['week'] >= '2018-01-01'].copy()


current_ids = current_ids['player_id']
current_ids






# Get list of player names matching IDs in current_ids


player_list_pt1 = matches3[((matches3['player_1_id'].isin(current_ids))


							 & (matches3['player_2_id'].isin(current_ids)))]['player_1']



player_list_pt2 = matches3[((matches3['player_1_id'].isin(current_ids))


							 & (matches3['player_2_id'].isin(current_ids)))]['player_2']



player_list = pd.concat([player_list_pt1, player_list_pt2])


player_list = sorted(player_list.unique().tolist())


# player_list






