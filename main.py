from player_parser import PlayerParser
from url_extractor import urlExtractor

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

team_url = "https://www.transfermarkt.com.tr/galatasaray/startseite/verein/141"
league_url = "https://www.transfermarkt.com.tr/super-lig/startseite/wettbewerb/TR1"

if __name__ == "__main__":

    teams_url = urlExtractor().getTeams(league_url=league_url, headers=headers)
    for team in teams_url:
        players_url = urlExtractor().getPlayers(team_url=team, headers=headers)
        for player_url in players_url:
            entry = PlayerParser().getAchievements(player_url, headers=headers)
            print(entry.name, entry.achievements)


