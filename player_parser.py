from bs4 import BeautifulSoup
import requests
from entry_format import Player

class PlayerParser():

    def getAchievements(self, url, headers):

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("tr", class_="hauptlink")

        blocks = soup.select("tr")
        achievements = []
        title_text = None

        for block in blocks:

            if "bg_Sturm" in block.get("class", []):
                title_text = block.text.strip()
                title_text = title_text.split("x", 1)[1].strip()

            else:
                try:
                    year = block.find("td", class_="erfolg_table_saison").text
                    team = block.find_all("td")
                    team = team[2].text.strip()
                except:
                    pass
                if title_text and year and team:
                    achievements.append(
                        {"name": title_text,
                         "year": year,
                         "team": team}
                    )

        player_id = soup.find("tm-watchlist")["player-id"]
        player_name = soup.find("h1", class_ = "data-header__headline-wrapper").text.replace(" ","").strip()
        player_jersey_no = player_name.split("\n", 1)[0].replace("#", "")
        try:
            player_name = player_name.split("\n", 1)[1]
        except:
            player_jersey_no = None

        entry = {}
        entry[player_id] = achievements

        current_team = soup.find("span", class_= "data-header__club").text.replace(" ","").strip()
        current_league = soup.find("span", class_ = "data-header__league").text.replace(" ","").strip()


        player = Player(player_id=player_id,
                        name=player_name,
                        achievements=achievements,
                        jersey_no=player_jersey_no,
                        current_team=current_team,
                        current_league=current_league)
        return player

