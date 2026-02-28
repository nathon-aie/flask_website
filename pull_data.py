import requests
import json
from main import app, db, Servant  # ดึงค่ามาจาก app.py


def fetch_and_save_data():
    # คำสั่ง app.app_context() จำเป็นมาก เพื่อให้ Flask รู้ว่าเรากำลังเชื่อมต่อ DB ของโปรเจกต์ไหน
    with app.app_context():
        # สร้างไฟล์/ตารางฐานข้อมูลถ้ายังไม่มี
        db.drop_all()  # ลบข้อมูลเก่าออกก่อน เพื่อให้ได้ข้อมูลใหม่ทุกครั้งที่รัน
        db.create_all()

        if Servant.query.count() == 0:
            print("[-] Pulling Data from Atlas Academy API...")

            url = "https://api.atlasacademy.io/export/NA/nice_servant.json"
            response = requests.get(url)
            all_servants = response.json()

            valid_servants = [
                s for s in all_servants if s["type"] in ["normal", "heroine"]
            ]

            valid_servants = sorted(valid_servants, key=lambda x: x["collectionNo"])
            valid_servants = valid_servants[1:]  # servant ตัวแรกเป็น dummy data ที่ไม่ต้องการ

            for data in valid_servants:
                raw_traits = data.get("traits", [])
                trait_names = [t["name"] for t in raw_traits]
                traits_string = ", ".join(trait_names)
                costume_dict = (
                    data.get("extraAssets", {}).get("charaGraph", {}).get("costume", {})
                )
                costume_urls = list(costume_dict.values())
                costume_string = ",".join(costume_urls)

                raw_mats = data.get("ascensionMaterials", {})
                processed_mats = {}
                for asc_level, mat_data in raw_mats.items():
                    display_level = str(int(asc_level) + 1)  # เปลี่ยน "0" เป็น "1" ให้ดูง่าย
                    level_items = []

                    for item_req in mat_data.get("items", []):
                        level_items.append(
                            {
                                "name": item_req["item"]["name"],
                                "icon": item_req["item"]["icon"],
                                "amount": item_req["amount"],
                            }
                        )
                    processed_mats[display_level] = level_items
                mats_json_string = json.dumps(processed_mats)

                raw_skill_mats = data.get("skillMaterials", {})
                processed_skill_mats = {}
                for level, mat_data in raw_skill_mats.items():
                    # ปรับข้อความให้ดูง่าย เช่น "Lv. 1 → 2"
                    display_level = f"Lv. {level} → {int(level) + 1}"
                    level_items = []
                    for item_req in mat_data.get("items", []):
                        level_items.append(
                            {
                                "name": item_req["item"]["name"],
                                "icon": item_req["item"]["icon"],
                                "amount": item_req["amount"],
                            }
                        )
                    processed_skill_mats[display_level] = level_items
                skill_mats_json = json.dumps(processed_skill_mats)

                raw_apd_skill_mats = data.get("appendSkillMaterials", {})
                processed_apd_skill_mats = {}
                for level, mat_data in raw_apd_skill_mats.items():
                    # ปรับข้อความให้ดูง่าย เช่น "Lv. 1 → 2"
                    display_level = f"Lv. {level} → {int(level) + 1}"
                    level_items = []
                    for item_req in mat_data.get("items", []):
                        level_items.append(
                            {
                                "name": item_req["item"]["name"],
                                "icon": item_req["item"]["icon"],
                                "amount": item_req["amount"],
                            }
                        )
                    processed_apd_skill_mats[display_level] = level_items
                apd_skill_mats_json = json.dumps(processed_apd_skill_mats)

                raw_skills = data.get("skills", [])
                processed_skills = []
                for skill in raw_skills:
                    processed_skills.append(
                        {
                            "num": skill.get("num"),  # ช่องของสกิล (1, 2 หรือ 3)
                            "name": skill.get("name"),  # ชื่อสกิล
                            "icon": skill.get("icon"),  # รูปไอคอนสกิล
                            "detail": skill.get("detail"),  # คำอธิบายสกิล
                            "cooldown": skill.get(
                                "coolDown"
                            ),  # คูลดาวน์ (เป็น List เช่น [7,7,7,6...])
                        }
                    )
                # เรียงสกิลตามช่อง (Slot 1 -> 2 -> 3)
                processed_skills = sorted(processed_skills, key=lambda x: x["num"])
                skills_json = json.dumps(processed_skills)

                new_servant = Servant(
                    servant_id=data["collectionNo"],
                    name=data["name"],
                    class_name=data["className"],
                    graph_url_asc1=data["extraAssets"]["charaGraph"]["ascension"]["1"],
                    graph_url_asc2=data["extraAssets"]["charaGraph"]["ascension"]["2"],
                    graph_url_asc3=data["extraAssets"]["charaGraph"]["ascension"]["3"],
                    graph_url_asc4=data["extraAssets"]["charaGraph"]["ascension"]["4"],
                    rarity=data["rarity"],
                    cost=data["cost"],
                    atk_base=data["atkBase"],
                    atk_max=data["atkMax"],
                    hp_base=data["hpBase"],
                    hp_max=data["hpMax"],
                    gender=data["gender"],
                    attribute=data["attribute"],
                    traits=traits_string,
                    costume=costume_string,
                    active_skill=skills_json,
                    ascension_materials=mats_json_string,
                    skill_materials=skill_mats_json,
                    append_skill_materials=apd_skill_mats_json,
                )
                db.session.add(new_servant)

            db.session.commit()
            print("[+] Saved on SQLite, pulling", len(valid_servants), "servants...")
        else:
            print("[!] Already have data in the database, skipping pull.")


if __name__ == "__main__":
    fetch_and_save_data()
