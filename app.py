# นำเข้า Flask framework และ render_template สำหรับแสดงผลหน้าเว็บ
from flask import Flask, render_template

# นำเข้า database และ model Servant
from models import db, Servant

# นำเข้าฟังก์ชันช่วยคำนวณวัสดุ
from utils import calculate_total_materials

# สร้าง Flask application
app = Flask(__name__)
# ตั้งค่าเส้นทางฐานข้อมูล SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///servants.db"
# ปิด track modifications เพื่อประหยัดหน่วยความจำ
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# เริ่มต้น database กับ Flask app
db.init_app(app)


# Route หลักและ route สำหรับแสดง Servant ทั้งหมด
@app.route("/")
@app.route("/class/all")
def index():
    # ดึงข้อมูล Servant ทั้งหมดจากฐานข้อมูล
    servants = Servant.query.all()
    # ส่งข้อมูลไปแสดงผลที่หน้า index.html
    return render_template("index.html", servants=servants)


# Route สำหรับกรอง Servant ตาม Class (เช่น Saber, Archer)
@app.route("/class/<class_name>")
def class_page(class_name):
    # ค้นหา Servant ที่มี class_name ตรงกับที่ระบุ
    servants = Servant.query.filter_by(class_name=class_name).all()
    # ส่งข้อมูลไปแสดงผลที่หน้า index.html
    return render_template("index.html", servants=servants)


# Route สำหรับแสดงรายละเอียดของ Servant แต่ละตัว
@app.route("/servant/<int:servant_id>/<path:name>")
def servant_detail(servant_id, name):
    # ค้นหา Servant จาก ID หรือแสดงหน้า 404 ถ้าไม่เจอ
    servant = Servant.query.filter_by(servant_id=servant_id).first_or_404()

    # ใช้ฟังก์ชันจาก utils.py ช่วยจัดการข้อมูล Materials
    # คำนวณวัสดุสำหรับ Ascension (เลื่อนขั้น) แยกตามระดับและแบบรวม
    asc_mats, total_asc = calculate_total_materials(servant.ascension_materials)
    # คำนวณวัสดุสำหรับ Skill (ทักษะ) แยกตามระดับและแบบรวม
    skl_mats, total_skl = calculate_total_materials(servant.skill_materials)
    # คำนวณวัสดุสำหรับ Append Skill (ทักษะเสริม) แยกตามระดับและแบบรวม
    apd_mats, total_apd = calculate_total_materials(servant.append_skill_materials)

    # ส่งข้อมูลทั้งหมดไปแสดงผลที่หน้า servant_detail.html
    return render_template(
        "servant_detail.html",
        servant=servant,  # ข้อมูล Servant
        costume=servant.costumes_list,  # รายการชุดคอสตูม
        active_skills=servant.skills_list,  # ทักษะหลัก
        append_skills=servant.append_skills_list,  # ทักษะเสริม
        noble_phantasms=servant.nps_list,  # Noble Phantasm
        ascension_materials=asc_mats,  # วัสดุ Ascension แยกตามระดับ
        total_ascension_materials=total_asc,  # วัสดุ Ascension รวมทั้งหมด
        skill_materials=skl_mats,  # วัสดุ Skill แยกตามระดับ
        total_skill_materials=total_skl,  # วัสดุ Skill รวมทั้งหมด
        append_skill_materials=apd_mats,  # วัสดุ Append Skill แยกตามระดับ
        total_append_skill_materials=total_apd,  # วัสดุ Append Skill รวมทั้งหมด
    )


# รันแอปพลิเคชันในโหมด debug เมื่อรันไฟล์นี้โดยตรง
if __name__ == "__main__":
    app.run(debug=True)
