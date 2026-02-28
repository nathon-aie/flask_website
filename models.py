# นำเข้า SQLAlchemy สำหรับจัดการฐานข้อมูล
from flask_sqlalchemy import SQLAlchemy
import json

# สร้างอินสแตนซ์ของ SQLAlchemy
db = SQLAlchemy()


# Model สำหรับเก็บข้อมูล Servant (ตัวละครในเกม Fate/Grand Order)
class Servant(db.Model):
    # Primary Key ของตาราง (Auto increment)
    id = db.Column(db.Integer, primary_key=True)
    # ID ของ Servant (ไม่ซ้ำกัน)
    servant_id = db.Column(db.Integer, unique=True)
    # ชื่อของ Servant (จำเป็นต้องมี)
    name = db.Column(db.String(100), nullable=False)
    # Class ของ Servant เช่น Saber, Archer (จำเป็นต้องมี)
    class_name = db.Column(db.String(50), nullable=False)
    # URL รูปภาพสำหรับแต่ละขั้น Ascension (1-4)
    graph_url_asc1 = db.Column(db.String(255))
    graph_url_asc2 = db.Column(db.String(255))
    graph_url_asc3 = db.Column(db.String(255))
    graph_url_asc4 = db.Column(db.String(255))
    # ระดับความหายาก (1-5 ดาว)
    rarity = db.Column(db.Integer)
    # จำนวน Cost ที่ใช้ในการจัดทีม
    cost = db.Column(db.Integer)
    # ค่า ATK ตอนเริ่มต้น
    atk_base = db.Column(db.Integer)
    # ค่า ATK สูงสุด
    atk_max = db.Column(db.Integer)
    # ค่า HP ตอนเริ่มต้น
    hp_base = db.Column(db.Integer)
    # ค่า HP สูงสุด
    hp_max = db.Column(db.Integer)
    # เพศของตัวละคร
    gender = db.Column(db.String(20))
    # Attribute (Man, Earth, Sky, Star, Beast)
    attribute = db.Column(db.String(20))
    # คุณสมบัติพิเศษต่างๆ (Traits)
    traits = db.Column(db.String(500))
    # URL ของรูปชุดคอสตูมต่างๆ (เก็บเป็น comma-separated string)
    costume = db.Column(db.Text)
    # ข้อมูลทักษะหลัก (เก็บเป็น JSON string)
    active_skill = db.Column(db.Text)
    # ข้อมูลทักษะเสริม (เก็บเป็น JSON string)
    append_skill = db.Column(db.Text)
    # ข้อมูล Noble Phantasm (เก็บเป็น JSON string)
    noble_phantasms = db.Column(db.Text)
    # วัสดุที่ใช้ในการ Ascension (เก็บเป็น JSON string)
    ascension_materials = db.Column(db.Text)
    # วัสดุที่ใช้ในการเลเวลทักษะ (เก็บเป็น JSON string)
    skill_materials = db.Column(db.Text)
    # วัสดุที่ใช้ในการเลเวลทักษะเสริม (เก็บเป็น JSON string)
    append_skill_materials = db.Column(db.Text)

    # ใช้ Property เพื่อให้เรียกใช้ข้อมูล JSON ได้ทันทีโดยไม่ต้อง json.loads ซ้ำใน Route

    @property
    def costumes_list(self):
        """แปลง costume จาก comma-separated string เป็น list"""
        return self.costume.split(",") if self.costume else []

    @property
    def skills_list(self):
        """แปลง active_skill จาก JSON string เป็น list"""
        return json.loads(self.active_skill) if self.active_skill else []

    @property
    def append_skills_list(self):
        """แปลง append_skill จาก JSON string เป็น list"""
        return json.loads(self.append_skill) if self.append_skill else []

    @property
    def nps_list(self):
        """แปลง noble_phantasms จาก JSON string เป็น list"""
        return json.loads(self.noble_phantasms) if self.noble_phantasms else []
