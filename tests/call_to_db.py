from pymongo import MongoClient
import pandas as pd


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

    print(res)


if __name__ == '__main__':
    __get_data_from_db(1610612737)
