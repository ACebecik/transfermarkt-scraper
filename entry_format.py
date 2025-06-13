from mongoengine import Document, StringField, IntField, ListField, DictField

class Player(Document):
    player_id = IntField(required=True, unique=True)
    name = StringField(required=True)
    achievements = ListField(DictField(StringField()))
    jersey_no = IntField()
    current_team = StringField()
    current_league = StringField()
