
from flask import jsonify
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamplayerdashboard, playercareerstats
import json

import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from pickle import load

fileName = "history_dataset.csv"
modelName = "./api/modelNBATrained_50.h5"
random_state = 42

def predict(home,away):
    current_season = '2023-24'
    selected_columns = ['GP', 'GS', 'MIN', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    num_stats = len(selected_columns)

    home_team = home
    away_team = away
    teams_query= [home_team, away_team]
    season = current_season

    array_1 = np.array([0.0] * num_stats)
    array_2 = np.array([0.0] * num_stats)
    teams_stats = [array_1, array_2]

    for idx, team in enumerate(teams_query):
        t1 = teams.find_teams_by_full_name(team)
        team_id = t1[0]['id']
        print("TEAM ID",team_id)

        t = teamplayerdashboard.TeamPlayerDashboard(team_id=team_id, season=season)
        data_player = json.loads(t.get_json())['resultSets']
        players_data = next(item for item in data_player if item['name'] == 'PlayersSeasonTotals')['rowSet']
        player_ids = [player[1] for player in players_data]
        print(f"PLAYER IDS:{player_ids}\n")

        for player_id in player_ids:
            print(f"PLAYER ID:{player_id}\n")
            career = playercareerstats.PlayerCareerStats(player_id=player_id)
            df_single_player_carrer = career.get_data_frames()[0]
            last_row_stats = df_single_player_carrer[selected_columns].iloc[-1].tolist()
            #print(f"{last_row_stats}")
            teams_stats[idx] += np.array(last_row_stats)
    print("end")
    pred_df = pd.DataFrame()
    # Aggiungere le statistiche al DataFrame
    for j, stat in enumerate(selected_columns):
        pred_df.loc[0, f'Home_Stat_{stat}'] = teams_stats[0][j]
        pred_df.loc[0, f'Away_Stat_{stat}'] = teams_stats[1][j]
    with open('./api/standardScaler_ready.pkl','rb') as f:
        scaler = load(f)
    
    X_std = scaler.transform(pred_df)
    model = load_model(modelName)
    res_tensor = model(X_std)
    res_int = round(res_tensor.numpy().item())
    res_int
    if res_int == 1:
        print(f"Ha vinto la squadra: {teams_query[0]}")
        result = {
            'winner': teams_query[0],
        }
    else:
        print(f"Ha vinto la squadra: {teams_query[1]}")
        result = {
            'winner': teams_query[1],
        }
    return jsonify(result)

