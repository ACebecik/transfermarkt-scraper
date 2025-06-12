
from player_parser import PlayerParser

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
url = "https://www.transfermarkt.com/emiliano-martinez/erfolge/spieler/111873"
titles = []
res = {}

if __name__ == "__main__":

    entry = PlayerParser().getAchievements(url, headers)
    print(entry.current_league)


