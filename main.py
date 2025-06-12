from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
url = "https://www.transfermarkt.com/leroy-sane/erfolge/spieler/192565"
titles = []
res = {}

if __name__ == "__main__":

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("tr", class_ = "hauptlink")

    for job in jobs:
       titles.append(job.text)

    player_id = soup.find("tm-watchlist")["player-id"]
    res[player_id] = titles

    blocks = soup.select("tr")

    achievements = []

    title_text = None

    for block in blocks:

        if "bg_Sturm" in block.get("class", []):
            title_text = block.text.strip()
            title_text = title_text.split("x", 1)[1].strip()

        else:
            try:
                year = block.find("td", class_= "erfolg_table_saison").text
                team = block.find_all("td")
                team = team[2].text.strip()
            except:
                pass
            if title_text and year and team :
                print(title_text, year, team)

