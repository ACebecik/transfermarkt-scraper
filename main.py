from player_parser import PlayerParser
from url_extractor import urlExtractor
from mongoengine import connect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

team_url = "https://www.transfermarkt.com.tr/galatasaray/startseite/verein/141"
league_url = "https://www.transfermarkt.com.tr/super-lig/startseite/wettbewerb/TR1"

uri = "mongodb+srv://Cluster58101:alperen78@cluster58101.jmvst6e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster58101"

client = connect("tmarkt", host=uri)
# Create a new client and connect to the server
db = client["tmarkt"]

# Select your collection (like a table)
collection = db["players"]

if __name__ == "__main__":

    teams_url = urlExtractor().getTeams(league_url=league_url, headers=headers)
    for team in teams_url:
        players_url = urlExtractor().getPlayers(team_url=team, headers=headers)
        for player_url in players_url:
            try:
                entry = PlayerParser().getAchievements(player_url, headers=headers)
                print(entry.name, entry.achievements)
                entry.save()
            except:
                print(f"skipped player: {entry.name}")






