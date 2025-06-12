import requests
from bs4 import BeautifulSoup

class urlExtractor():

    def __init__(self):
        self.base_url = "https://www.transfermarkt.com"
    def getTeams(self, league_url):
        pass

    def getPlayers(self, team_url, headers):

        response = requests.get(url=team_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("td", class_="hauptlink")
        player_urls = []
        for j in jobs:
            url = j.find("a")["href"]
            if "profil/spieler" in url:
                url = url.replace("profil", "erfolge")
                player_urls.append(self.base_url + url)

        return player_urls

if __name__ == "__main__":

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    url = "https://www.transfermarkt.com/aston-villa/startseite/verein/405"
    player_urls = urlExtractor().getPlayers(url, headers)
    print(player_urls)

