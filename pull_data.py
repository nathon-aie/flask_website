# นำเข้า libraries ที่จำเป็น
import requests  # สำหรับดึงข้อมูลจาก API
import json  # สำหรับจัดการข้อมูล JSON
import re  # สำหรับ Regular Expression
from app import app  # นำเข้า Flask app
from models import db, Servant  # นำเข้า database และ model


def fetch_and_save_data():
    """ฟังก์ชันหลักสำหรับดึงข้อมูล Servant จาก API และบันทึกลงฐานข้อมูล"""
    with app.app_context():
        # ลบตารางเก่าและสร้างตารางใหม่
        db.drop_all()
        db.create_all()

        print("[-] Pulling Data from Atlas Academy API...")
        # URL ของ API ที่เก็บข้อมูล Servant ทั้งหมด (เวอร์ชัน North America)
        url = "https://api.atlasacademy.io/export/NA/nice_servant.json"
        # ดึงข้อมูลจาก API และแปลงเป็น JSON
        all_servants = requests.get(url).json()

        # กรองเฉพาะ Servant ประเภท normal และ heroine (ไม่รวม enemy, svtEquip)
        valid_servants = [s for s in all_servants if s["type"] in ["normal", "heroine"]]
        # เรียงตาม Collection Number และตัดตัวแรกออก (ตัวแรกมักเป็น Mash หรือตัวพิเศษ)
        valid_servants = sorted(valid_servants, key=lambda x: x["collectionNo"])[1:]

        # วนลูปผ่าน Servant แต่ละตัว
        for data in valid_servants:
            # --- ส่วนประมวลผล Traits และ Costumes ---
            # รวม Traits ทั้งหมดเป็น string คั่นด้วย comma
            traits_string = ", ".join([t["name"] for t in data.get("traits", [])])
            # ดึง URL ของชุดคอสตูมทั้งหมด
            costume_urls = list(
                data.get("extraAssets", {})
                .get("charaGraph", {})
                .get("costume", {})
                .values()
            )

            # --- ฟังก์ชันภายในช่วยจัดการ Materials (Ascension/Skill/Append) ---
            def process_mats(raw_data, is_skill=False):
                """แปลงข้อมูลวัสดุจาก API เป็นรูปแบบที่ใช้งานง่าย

                Parameters:
                    raw_data: ข้อมูลวัสดุดิบจาก API
                    is_skill: True ถ้าเป็นวัสดุสำหรับทักษะ (จะใช้รูปแบบ Lv. X → Y)
                """
                processed = {}
                # วนลูปผ่านแต่ละระดับและข้อมูลวัสดุ
                for level, mat_data in raw_data.items():
                    # สร้าง key สำหรับแต่ละระดับ
                    key = (
                        f"Lv. {level} → {int(level) + 1}"  # สำหรับทักษะ: "Lv. 1 → 2"
                        if is_skill
                        else str(int(level) + 1)  # สำหรับ Ascension: "1", "2", "3", "4"
                    )
                    # สร้าง list ของไอเทมที่ต้องใช้ในระดับนั้น
                    processed[key] = [
                        {
                            "name": i["item"]["name"],  # ชื่อไอเทม
                            "icon": i["item"]["icon"],  # URL ไอคอน
                            "amount": i["amount"],  # จำนวนที่ต้องใช้
                        }
                        for i in mat_data.get("items", [])
                    ]
                # แปลงเป็น JSON string เพื่อบันทึกลงฐานข้อมูล
                return json.dumps(processed)

            # --- ประมวลผล Noble Phantasms ---
            nps = []
            for np in data.get("noblePhantasms", []):
                # ทำความสะอาด detail โดยแทนที่ {{...}} ด้วย [Lv. 1-5 / OC]
                clean_detail = re.sub(
                    r"\{\{.*?\}\}", "[Lv. 1-5 / OC]", np.get("detail", "")
                )
                # เพิ่มข้อมูล Noble Phantasm
                nps.append(
                    {
                        "name": np.get("name"),  # ชื่อ
                        "card": np.get("card"),  # ประเภทการ์ด (Buster, Arts, Quick)
                        "icon": np.get("icon"),  # URL ไอคอน
                        "detail": clean_detail,  # รายละเอียดเอฟเฟกต์
                        "rank": np.get("rank"),  # Rank (A, B, C, EX)
                        "type": np.get("type"),  # ประเภท (Anti-Unit, Anti-Army, etc.)
                    }
                )

            # สร้าง object Servant ใหม่พร้อมข้อมูลทั้งหมด
            new_servant = Servant(
                servant_id=data["collectionNo"],  # Collection Number
                name=data["name"],  # ชื่อ
                class_name=data["className"],  # Class
                # URL รูปภาพแต่ละขั้น Ascension
                graph_url_asc1=data["extraAssets"]["charaGraph"]["ascension"]["1"],
                graph_url_asc2=data["extraAssets"]["charaGraph"]["ascension"]["2"],
                graph_url_asc3=data["extraAssets"]["charaGraph"]["ascension"]["3"],
                graph_url_asc4=data["extraAssets"]["charaGraph"]["ascension"]["4"],
                rarity=data["rarity"],  # ระดับความหายาก (ดาว)
                cost=data["cost"],  # Cost
                atk_base=data["atkBase"],  # ATK เริ่มต้น
                atk_max=data["atkMax"],  # ATK สูงสุด
                hp_base=data["hpBase"],  # HP เริ่มต้น
                hp_max=data["hpMax"],  # HP สูงสุด
                gender=data["gender"],  # เพศ
                attribute=data["attribute"],  # Attribute
                traits=traits_string,  # Traits
                costume=",".join(costume_urls),  # URL ชุดคอสตูม (คั่นด้วย comma)
                # ข้อมูลทักษะหลัก (เรียงตามลำดับ num แล้วแปลงเป็น JSON)
                active_skill=json.dumps(
                    sorted(
                        [
                            {
                                "num": s["num"],  # เลขที่ทักษะ (1, 2, 3)
                                "name": s["name"],  # ชื่อทักษะ
                                "icon": s["icon"],  # URL ไอคอน
                                "detail": s["detail"],  # รายละเอียดเอฟเฟกต์
                                "cooldown": s.get("coolDown"),  # Cooldown (ระยะเวลารอ)
                            }
                            for s in data.get("skills", [])
                        ],
                        key=lambda x: x["num"],  # เรียงตาม num
                    )
                ),
                # ข้อมูลทักษะเสริม (Append Skills)
                append_skill=json.dumps(
                    sorted(
                        [
                            {
                                "num": a["num"],  # เลขที่ทักษะเสริม (1, 2, 3)
                                "name": a["skill"]["name"],  # ชื่อทักษะ
                                "icon": a["skill"]["icon"],  # URL ไอคอน
                                # ทำความสะอาด detail โดยแทนที่ {{...}} ด้วย [Lv. 1-10]
                                "detail": re.sub(
                                    r"\{\{.*?\}\}", "[Lv. 1-10]", a["skill"]["detail"]
                                ),
                            }
                            for a in data.get("appendPassive", [])
                        ],
                        key=lambda x: x["num"],  # เรียงตาม num
                    )
                ),
                # ข้อมูล Noble Phantasms (แปลงเป็น JSON)
                noble_phantasms=json.dumps(nps),
                # วัสดุสำหรับ Ascension (ใช้ฟังก์ชัน process_mats)
                ascension_materials=process_mats(data.get("ascensionMaterials", {})),
                # วัสดุสำหรับเลเวลทักษะหลัก (is_skill=True)
                skill_materials=process_mats(data.get("skillMaterials", {}), True),
                # วัสดุสำหรับเลเวลทักษะเสริม (is_skill=True)
                append_skill_materials=process_mats(
                    data.get("appendSkillMaterials", {}), True
                ),
            )
            # เพิ่ม Servant ลงในเซสชันของฐานข้อมูล
            db.session.add(new_servant)

        # บันทึกข้อมูลทั้งหมดลงฐานข้อมูล
        db.session.commit()
        print(f"[+] Saved {len(valid_servants)} servants to SQLite.")


# รันฟังก์ชันเมื่อเรียกไฟล์นี้โดยตรง
if __name__ == "__main__":
    fetch_and_save_data()
