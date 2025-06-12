import requests
from bs4 import BeautifulSoup

class urlExtractor():

    def __init__(self):
        self.base_url = "https://www.transfermarkt.com"
    def getTeams(self, league_url, headers):
        response = requests.get(url = league_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        teams = soup.find_all("td", class_ = "hauptlink no-border-links")
        teams_urls = []

        for team in teams:
            url = team.find("a")["href"]
            teams_urls.append(self.base_url + url)

        return teams_urls


    def getPlayers(self, team_url, headers):

        response = requests.get(url=team_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        players = soup.find_all("td", class_="hauptlink")
        player_urls = []
        for p in players:
            try:
                url = p.find("a")["href"]
                if "profil/spieler" in url:
                    url = url.replace("profil", "erfolge")
                    player_urls.append(self.base_url + url)
            except:
                pass

        return player_urls

if __name__ == "__main__":

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    url = "https://www.transfermarkt.com.tr/super-lig/startseite/wettbewerb/TR1"
    #team_urls = urlExtractor().getTeams(url, headers)
    url = "https://www.transfermarkt.com.tr/besiktas-istanbul/startseite/verein/114/saison_id/2024"
    print(urlExtractor().getPlayers(url, headers))

