from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class Servant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servant_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    graph_url_asc1 = db.Column(db.String(255))
    graph_url_asc2 = db.Column(db.String(255))
    graph_url_asc3 = db.Column(db.String(255))
    graph_url_asc4 = db.Column(db.String(255))
    rarity = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    atk_base = db.Column(db.Integer)
    atk_max = db.Column(db.Integer)
    hp_base = db.Column(db.Integer)
    hp_max = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    attribute = db.Column(db.String(20))
    traits = db.Column(db.String(500))
    costume = db.Column(db.Text)
    active_skill = db.Column(db.Text)
    append_skill = db.Column(db.Text)
    noble_phantasms = db.Column(db.Text)
    ascension_materials = db.Column(db.Text)
    skill_materials = db.Column(db.Text)
    append_skill_materials = db.Column(db.Text)

    # ใช้ Property เพื่อให้เรียกใช้ข้อมูล JSON ได้ทันทีโดยไม่ต้อง json.loads ซ้ำใน Route
    @property
    def costumes_list(self):
        return self.costume.split(",") if self.costume else []

    @property
    def skills_list(self):
        return json.loads(self.active_skill) if self.active_skill else []

    @property
    def append_skills_list(self):
        return json.loads(self.append_skill) if self.append_skill else []

    @property
    def nps_list(self):
        return json.loads(self.noble_phantasms) if self.noble_phantasms else []
