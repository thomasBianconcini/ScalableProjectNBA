from pymongo import MongoClient
import pandas as pd


def main():
    connection_string = ("mongodb+srv://taylor:Vignolabrucia1@cosmosdbnbatest.mongocluster.cosmos.azure.com/?tls=true"
                         "&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000")
    client = MongoClient(connection_string)

    # Nome del nuovo database e della collezione
    db_name = "stats"
    collection_name = "teams_players"

    # Creazione del riferimento al database e alla collezione
    db = client[db_name]
    collection = db[collection_name]

    # Lettura del file CSV
    df = pd.read_csv('all_players_db.csv')

    # Trasformazione del DataFrame in una lista di dizionari
    records = df.to_dict(orient='records')

    # Inserimento dei dati nel database
    collection.insert_many(records)

    # Verifica dei database disponibili
    db_list = client.list_database_names()
    print("Databases disponibili:", db_list)

    # Stampa dei dati inseriti per conferma
    for doc in collection.find():
        print(doc)

    # Chiudere il client una volta completate le operazioni
    client.close()


if __name__ == "__main__":
    main()
