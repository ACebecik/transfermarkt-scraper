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
                if title_text and year and team and type(team) == str and type(year) == str and type(title_text) == str:
                    achievements.append(
                        {"name": title_text,
                         "year": year,
                         "team": team}
                    )

        player_id = int(soup.find("tm-watchlist")["player-id"])
        player_name = soup.find("h1", class_ = "data-header__headline-wrapper").text.replace(" ","").strip()
        try:
            player_jersey_no = int(player_name.split("\n", 1)[0].replace("#", ""))
            player_name = player_name.split("\n", 1)[1]
        except:
            player_jersey_no = 0

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


if __name__ == "__main__":

    headers = {
        'authority': 'www.transfermarkt.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,tr;q=0.7,de;q=0.6,it;q=0.5',
        'cache-control': 'max-age=0',
        'cookie': '_sp_su=false; _sp_v1_uid=1:536:ee8a68b0-0aae-42fb-bd3a-dc734e224d36; _sp_v1_ss=1:H4sIAAAAAAAAAItWqo5RKimOUbKKxmDklebk6MQopSKxS8AS1bW1sSRLKOngsQrEyAMxDMgwGbeVsQAb6zCm3wAAAA%3D%3D; TMSESSID=8ce1c279e4daaf3b3b1f926e943c45bc; euconsent-v2=CPsKuUAPsKuUAAGABCENDECsAP_AAH_AAAYgH4td_H_fbX9j-f596ft0eY1f9_rzruQzDheNk-4FyJ_W_LwXz2E7NB36pq4KmR4Eu1LBAQNlHMHUDQmwaIkVqTHsak2MpSNKJ6BEkHMZe2dYGFpPmxFD-QKY5t5_93b52D-9_dv-z9z338VXn3N538v0wAAAAIAAACAAAAAAAAIHBAEGAAIAAACCAAAACAEAAAIARIAAAAAAgAAoAAACBQABKwCEwEAABAIAIQAAQggIQIBAAAAAEgAAAgBYIAAABAIAAQAAAAAACAAEBABICAAAAAEgAABAACBAARAAAUhAQEABBACgAAAAFEhgBAEWUABAWCQSAAEAALgAoACoAGQAOAAeABAADAAGUANAA1AB5AEMARQAmABPACqAG8AOYAegA_ACEAENAIgAiQBLACaAFKALcAYYAyABlgDZAHeAPYAfEA-wD9gH-AgABFICLgIwARwAkwBKQCggFPAKuAXMAxQBrADaAG4APkAh0BIgCZQE7AKHAUeApEBTQCxQFsALkAXeAvMBgwDDQGSAMnAZcAzkBnwDSIGsAayA28KABAEUEAFAAbABIAUsAs4BogE2AKbAW4AwIBtQaA0AFwAQwAyABlgDZgH2AfgBAACCgEYAJMAU8Aq8BaAFpANYAdUA-QCHQEVAJEATsApEBcgDJwGcgM8AZ8GABgJsAU2A2odBZAAXABQAFQAMgAcABAAC6AGAAZQA0ADUAHgAPoAhgCKAEwAJ4AVQAuABiADMAG8AOYAegA_ACGgEQARIAlgBNACjAFKALEAW8AwgDDAGQAMoAaIA2QB3gD2gH2AfoA_wCKQEXARiAjgCOgEmAJSAUEAp4BVwCxQFoAWkAuYBeQDFAG0ANwAc4A6gB9gEOgIqAReAkQBKgCZAE7AKHAUeApoBVgCxQFsALgAXIAu0Bd4C8wGDAMNAY9AyMDJAGTgMqAZYAy4BmYDOQGfANEAaQA1gBt48AEAIoAjI4AQABcAEgAUADMgJsAU2AtwBtQiAsAIYAZAAywBswD7APwAgABGACTAFPAKuAawA6oB8gEOgJEATsApEBcgDIwGTgM5AZ8IABgAkATYA2oVARAAoAEMAJgAXABHADLAI4AVeAtAC0gLYAXIAvMBkYDOQGeAM-AbkKABAJsAbUMgHgBDACYAI4AZYBHACrgFbAWiAtgBcgC8wGRgM5AZ4Az4YACATYA2ohA0AAWABQADIALgAYgA1ACGAEwAKYAVQAuABiADMAG8APQAjgBSgCxAGEAMoAd4A-wB_gEUAI4ASkAoIBTwCrwFoAWkAuYBigDaAHOAOoAkQBKgCmgFWALFAWiAtgBcAC5AF2gMjAZOAzkBngDPgGiAOAIgAgCMgJiIABABmgGZATYA2olA0AAQAAsACgAGQAOAAfgBgAGIAPAAiABMACqAFwAMQAZgBDQCIAIkAUYApQBbgDCAGUANkAd8A-wD8AI4AU8Aq8BaAFpALmAYoA3AB1AD5AIdARUAi8BIgCjwFigLYAXaAvMBkYDJwGWAM5AZ4Az4BpADWAG3gOAJgAQCMkgAoAFwBmgGZATYAtwpBBAAXABQAFQAMgAcABBADAAMoAaABqADyAIYAigBMACeAFIAKoAYgAzABzAD8AIaARABEgCjAFKALEAW4AwgBkADKAGiANkAd8A-wD9AIxARwBHQCUgFBAKuAVsAuYBeQDaAG4APsAh0BF4CRAEnAJ2AUOAqwBYoC2AFwALkAXaAvMBhsDIwMkAZOAywBlwDOQGeAM-AaRA1gDWQG3lABAAFwASAB_AIOAScBNgCmwFuA.YAAAAAAAAAAA; consentUUID=977d35cd-fb92-4278-ae2e-e3759b9af752_14_15_19; _sp_v1_data=2:584042:1684789607:0:1:-1:1:0:0:_:-1; _sp_v1_opt=1:login|true:last_id|11:; _sp_v1_csv=; _sp_v1_lt=1:; _tmlpu=5',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    print(PlayerParser().getAchievements("https://www.transfermarkt.com.tr/arlind-ajeti/erfolge/spieler/159288", headers=headers).achievements)