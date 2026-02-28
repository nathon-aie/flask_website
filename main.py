from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///servants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# โครงสร้างตารางฐานข้อมูล
class Servant(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ใช้ id เป็น primary key อัตโนมัติ
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
    traits = db.Column(db.String(500))  # เพิ่มคอลัมน์ traits เพื่อเก็บข้อมูล traits
    costume = db.Column(db.Text)  # เพิ่มคอลัมน์ costume เพื่อเก็บข้อมูล costume
    active_skill = db.Column(db.Text)
    ascension_materials = db.Column(db.Text)
    skill_materials = db.Column(db.Text)
    append_skill_materials = db.Column(db.Text)


@app.route("/")
@app.route("/class/all")
def index():
    servants = Servant.query.all()
    return render_template("index.html", servants=servants)


@app.route("/class/<class_name>")
def class_page(class_name):
    servants = Servant.query.filter_by(class_name=class_name).all()
    return render_template("index.html", servants=servants)


@app.route("/servant/<int:servant_id>/<path:name>")
def servant_detail(servant_id, name):
    # ดึงข้อมูลจากฐานข้อมูลเฉพาะตัวที่ ID ตรงกับที่คลิกเข้ามา
    servant = Servant.query.filter_by(servant_id=servant_id).first()

    costume_list = []
    if servant and servant.costume:
        costume_list = servant.costume.split(",")

    asc_mats = {}
    total_asc_mats_dict = {}
    if servant and servant.ascension_materials:
        asc_mats = json.loads(servant.ascension_materials)
        for level, items in asc_mats.items():
            for item in items:
                name = item["name"]
                if name in total_asc_mats_dict:
                    # ถ้ามีชื่อไอเทมนี้อยู่แล้ว ให้บวกจำนวนเพิ่ม
                    total_asc_mats_dict[name]["amount"] += item["amount"]
                else:
                    # ถ้ายังไม่มี ให้สร้างใหม่
                    total_asc_mats_dict[name] = {
                        "name": name,
                        "icon": item["icon"],
                        "amount": item["amount"],
                    }
    # แปลงจาก Dictionary กลับเป็น List เพื่อให้เอาไปวนลูปใน HTML ง่ายๆ
    total_asc_mats = list(total_asc_mats_dict.values())

    skl_mats = {}
    total_skl_mats_dict = {}
    if servant and servant.skill_materials:
        skl_mats = json.loads(servant.skill_materials)
        for level, items in skl_mats.items():
            for item in items:
                name = item["name"]
                if name in total_skl_mats_dict:
                    # ถ้ามีชื่อไอเทมนี้อยู่แล้ว ให้บวกจำนวนเพิ่ม
                    total_skl_mats_dict[name]["amount"] += item["amount"]
                else:
                    # ถ้ายังไม่มี ให้สร้างใหม่
                    total_skl_mats_dict[name] = {
                        "name": name,
                        "icon": item["icon"],
                        "amount": item["amount"],
                    }
    # แปลงจาก Dictionary กลับเป็น List เพื่อให้เอาไปวนลูปใน HTML ง่ายๆ
    total_skl_mats = list(total_skl_mats_dict.values())

    apd_skl_mats = {}
    total_apd_skl_mats_dict = {}
    if servant and servant.append_skill_materials:
        apd_skl_mats = json.loads(servant.append_skill_materials)
        for level, items in apd_skl_mats.items():
            for item in items:
                name = item["name"]
                if name in total_apd_skl_mats_dict:
                    # ถ้ามีชื่อไอเทมนี้อยู่แล้ว ให้บวกจำนวนเพิ่ม
                    total_apd_skl_mats_dict[name]["amount"] += item["amount"]
                else:
                    # ถ้ายังไม่มี ให้สร้างใหม่
                    total_apd_skl_mats_dict[name] = {
                        "name": name,
                        "icon": item["icon"],
                        "amount": item["amount"],
                    }
    # แปลงจาก Dictionary กลับเป็น List เพื่อให้เอาไปวนลูปใน HTML ง่ายๆ
    total_apd_skl_mats = list(total_apd_skl_mats_dict.values())

    skills = []
    if servant and servant.active_skills:
        skills = json.loads(servant.active_skills)

    return render_template(
        "servant_detail.html",
        servant=servant,
        costume=costume_list,
        active_skills=skills,
        ascension_materials=asc_mats,
        total_ascension_materials=total_asc_mats,
        skill_materials=skl_mats,
        total_skill_materials=total_skl_mats,
        append_skill_materials=apd_skl_mats,
        total_append_skill_materials=total_apd_skl_mats,
    )


if __name__ == "__main__":
    app.run(debug=True)
