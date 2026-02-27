import requests
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
                new_servant = Servant(
                    servant_id=data["collectionNo"],
                    name=data["name"],
                    class_name=data["className"],
                    graph_url_asc1=data["extraAssets"]["charaGraph"]["ascension"]["1"],
                    graph_url_asc2=data["extraAssets"]["charaGraph"]["ascension"]["2"],
                    graph_url_asc3=data["extraAssets"]["charaGraph"]["ascension"]["3"],
                    graph_url_asc4=data["extraAssets"]["charaGraph"]["ascension"]["4"],
                    rarity=data["rarity"],
                    atk_max=data["atkMax"],
                    hp_max=data["hpMax"],
                )
                db.session.add(new_servant)

            db.session.commit()
            print("[+] Saved on SQLite, pulling", len(valid_servants), "servants...")
        else:
            print("[!] Already have data in the database, skipping pull.")


if __name__ == "__main__":
    fetch_and_save_data()
