from flask import jsonify
from pymongo import MongoClient

import pandas as pd
from tensorflow.keras.models import load_model
from pickle import load

fileName = "history_dataset.csv"
modelName = "./model/modelNBATrained_50.h5"
random_state = 42

TEAM_IDS = {
    "Atlanta Hawks": 1610612737,
    "Boston Celtics": 1610612738,
    "Brooklyn Nets": 1610612751,
    "Charlotte Hornets": 1610612766,
    "Chicago Bulls": 1610612741,
    "Cleveland Cavaliers": 1610612739,
    "Dallas Mavericks": 1610612742,
    "Denver Nuggets": 1610612743,
    "Detroit Pistons": 1610612765,
    "Golden State Warriors": 1610612744,
    "Houston Rockets": 1610612745,
    "Indiana Pacers": 1610612754,
    "Los Angeles Clippers": 1610612746,
    "Los Angeles Lakers": 1610612747,
    "Memphis Grizzlies": 1610612763,
    "Miami Heat": 1610612748,
    "Milwaukee Bucks": 1610612749,
    "Minnesota Timberwolves": 1610612750,
    "New Orleans Pelicans": 1610612740,
    "New York Knicks": 1610612752,
    "Oklahoma City Thunder": 1610612760,
    "Orlando Magic": 1610612753,
    "Philadelphia 76ers": 1610612755,
    "Phoenix Suns": 1610612756,
    "Portland Trail Blazers": 1610612757,
    "Sacramento Kings": 1610612758,
    "San Antonio Spurs": 1610612759,
    "Toronto Raptors": 1610612761,
    "Utah Jazz": 1610612762,
    "Washington Wizards": 1641062764
}


def __get_data_from_db(team_id):
    connection_string = ("mongodb+srv://taylor:Vignolabrucia1@cosmosdbnbatest.mongocluster.cosmos.azure.com/?tls=true"
                         "&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000")
    client = MongoClient(connection_string)

    # Nome del nuovo database e della collezione
    db_name = "stats"
    collection_name = "teams_players"

    # Creazione del riferimento al database e alla collezione
    db = client[db_name]
    collection = db[collection_name]

    data = collection.find({"TEAM_ID": team_id})

    res = pd.DataFrame(list(data))
    client.close()

    return res


def predict(home, away):
    selected_columns = ['GP', 'GS', 'MIN', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK',
                        'TOV', 'PF', 'PTS']

    # Creazione del DataFrame
    home_team_players = __get_data_from_db(TEAM_IDS[home])
    away_team_players = __get_data_from_db(TEAM_IDS[away])

    home_team_players = home_team_players.drop(columns=["TEAM_ID", "PLAYER_ID"])
    away_team_players = away_team_players.drop(columns=["TEAM_ID", "PLAYER_ID"])

    home_team_stats = home_team_players[selected_columns].sum().to_frame().T
    away_team_stats = away_team_players[selected_columns].sum().to_frame().T

    pred_df = pd.DataFrame()

    for j, stat in enumerate(selected_columns):
        pred_df.loc[0, f'Home_Stat_{stat}'] = home_team_stats.iloc[0][j]
        pred_df.loc[0, f'Away_Stat_{stat}'] = away_team_stats.iloc[0][j]

    print(pred_df)
        
    with open('./model/standardScaler_ready.pkl', 'rb') as f:
        scaler = load(f)

    X_std = scaler.transform(pred_df)
    model = load_model(modelName)
    res_tensor = model(X_std)
    res_int = round(res_tensor.numpy().item())

    if res_int == 1:
        result = {'winner': home}
    else:
        result = {'winner': away}

    return jsonify(result)
