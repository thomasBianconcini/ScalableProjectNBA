from locust import HttpUser, task, between
import random

team_names = [
    "Atlanta Hawks",
    "Boston Celtics",
    "Brooklyn Nets",
    "Charlotte Hornets",
    "Chicago Bulls",
    "Cleveland Cavaliers",
    "Dallas Mavericks",
    "Denver Nuggets",
    "Detroit Pistons",
    "Golden State Warriors",
    "Houston Rockets",
    "Indiana Pacers",
    "Los Angeles Clippers",
    "Los Angeles Lakers",
    "Memphis Grizzlies",
    "Miami Heat",
    "Milwaukee Bucks",
    "Minnesota Timberwolves",
    "New Orleans Pelicans",
    "New York Knicks",
    "Oklahoma City Thunder",
    "Orlando Magic",
    "Philadelphia 76ers",
    "Phoenix Suns",
    "Portland Trail Blazers",
    "Sacramento Kings",
    "San Antonio Spurs",
    "Toronto Raptors",
    "Utah Jazz"
]


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        # Disabilita la verifica del certificato SSL
        self.client.verify = False

    @task(3)
    def access_api(self):
        headers = {"X-API-KEY": "taylor"}
        # Selezione random di due squadre
        selected_teams = random.sample(team_names, 2)
        params = {"squadra1": selected_teams[0],
                  "squadra2": selected_teams[1]}

        self.client.get("/api/predict", headers=headers, params=params)
