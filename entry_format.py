from mongoengine import Document, StringField, IntField, ListField, DictField

class Player(Document):
    player_id = IntField(required=True)
    name = StringField(required=True)
    achievements = ListField(DictField(StringField()))
    jersey_no = IntField()
    current_team = StringField()
    current_league = StringField()
"""
    def __init__(self, player_id, name, achievements, jersey_no, current_team, current_league):
        self.player_id = player_id
        self.name = name
        self.achievements = achievements
        self.jersey_no = jersey_no
        self.current_team = current_team
        self.current_league = current_league
"""