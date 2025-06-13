from ensurepip import bootstrap

from player_parser import PlayerParser
from url_extractor import urlExtractor
from mongoengine import connect
from league_urls import leagues
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json

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

team_url = "https://www.transfermarkt.com.tr/galatasaray/startseite/verein/141"
league_url = "https://www.transfermarkt.com.tr/super-lig/startseite/wettbewerb/TR1"

uri = "mongodb+srv://Cluster58101:alperen78@cluster58101.jmvst6e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster58101"

client = connect("tmarkt", host=uri)
# Create a new client and connect to the server
db = client["tmarkt"]

# Select your collection (like a table)
collection = db["players"]
topic_name = "players-topic"

if __name__ == "__main__":


    producer = KafkaProducer(
        bootstrap_servers = "localhost:9092",
        value_serializer=str.encode
    )
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers="localhost:9092",
        value_deserializer = bytes.decode
    )

    teams_url = []
    players_url= []

    for league in leagues :
        #print(f"For league: {league}")
        while not teams_url:
            teams_url = urlExtractor().getTeams(league_url=league, headers=headers)
        for team in teams_url:
            print(f"For team {team}")
            while not players_url:
                players_url = urlExtractor().getPlayers(team_url=team, headers=headers)
            for player_url in players_url:
                print(player_url)
                producer.send(topic_name, value=player_url)
                producer.flush()
            players_url = []
        teams_url = []