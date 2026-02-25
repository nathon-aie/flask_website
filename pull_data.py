import requests
from main import app, db, Servant  # ดึงค่ามาจาก app.py


def fetch_and_save_data():
    # คำสั่ง app.app_context() จำเป็นมาก เพื่อให้ Flask รู้ว่าเรากำลังเชื่อมต่อ DB ของโปรเจกต์ไหน
    with app.app_context():
        # สร้างไฟล์/ตารางฐานข้อมูลถ้ายังไม่มี
        db.create_all()

        if Servant.query.count() == 0:
            print("[-] Pulling Data from Atlas Academy API...")

            url = "https://api.atlasacademy.io/export/NA/basic_servant.json"
            response = requests.get(url)
            all_servants = response.json()

            valid_servants = [
                s for s in all_servants if s["type"] in ["normal", "heroine"]
            ]

            for data in valid_servants:
                new_servant = Servant(
                    servant_id=data["collectionNo"],
                    name=data["name"],
                    class_name=data["className"],
                    face_url=data["face"],
                )
                db.session.add(new_servant)

            db.session.commit()
            print("[+] Saved on SQLite, pulling", len(valid_servants), "servants...")
        else:
            print("[!] Already have data in the database, skipping pull.")


if __name__ == "__main__":
    fetch_and_save_data()
