import requests
import json
import re
from app import app
from models import db, Servant


def fetch_and_save_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("[-] Pulling Data from Atlas Academy API...")
        url = "https://api.atlasacademy.io/export/NA/nice_servant.json"
        all_servants = requests.get(url).json()

        # กรองเฉพาะ Servant ปกติและเรียงตาม ID
        valid_servants = [s for s in all_servants if s["type"] in ["normal", "heroine"]]
        valid_servants = sorted(valid_servants, key=lambda x: x["collectionNo"])[1:]

        for data in valid_servants:
            # --- ส่วนประมวลผล Traits และ Costumes ---
            traits_string = ", ".join([t["name"] for t in data.get("traits", [])])
            costume_urls = list(
                data.get("extraAssets", {})
                .get("charaGraph", {})
                .get("costume", {})
                .values()
            )

            # --- ฟังก์ชันภายในช่วยจัดการ Materials (Ascension/Skill/Append) ---
            def process_mats(raw_data, is_skill=False):
                processed = {}
                for level, mat_data in raw_data.items():
                    key = (
                        f"Lv. {level} → {int(level) + 1}"
                        if is_skill
                        else str(int(level) + 1)
                    )
                    processed[key] = [
                        {
                            "name": i["item"]["name"],
                            "icon": i["item"]["icon"],
                            "amount": i["amount"],
                        }
                        for i in mat_data.get("items", [])
                    ]
                return json.dumps(processed)

            # --- ประมวลผล Noble Phantasms และ Skills ---
            nps = []
            for np in data.get("noblePhantasms", []):
                clean_detail = re.sub(
                    r"\{\{.*?\}\}", "[Lv. 1-5 / OC]", np.get("detail", "")
                )
                nps.append(
                    {
                        "name": np.get("name"),
                        "card": np.get("card"),
                        "icon": np.get("icon"),
                        "detail": clean_detail,
                        "rank": np.get("rank"),
                        "type": np.get("type"),
                    }
                )

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
                costume=",".join(costume_urls),
                active_skill=json.dumps(
                    sorted(
                        [
                            {
                                "num": s["num"],
                                "name": s["name"],
                                "icon": s["icon"],
                                "detail": s["detail"],
                                "cooldown": s.get("coolDown"),
                            }
                            for s in data.get("skills", [])
                        ],
                        key=lambda x: x["num"],
                    )
                ),
                append_skill=json.dumps(
                    sorted(
                        [
                            {
                                "num": a["num"],
                                "name": a["skill"]["name"],
                                "icon": a["skill"]["icon"],
                                "detail": re.sub(
                                    r"\{\{.*?\}\}", "[Lv. 1-10]", a["skill"]["detail"]
                                ),
                            }
                            for a in data.get("appendPassive", [])
                        ],
                        key=lambda x: x["num"],
                    )
                ),
                noble_phantasms=json.dumps(nps),
                ascension_materials=process_mats(data.get("ascensionMaterials", {})),
                skill_materials=process_mats(data.get("skillMaterials", {}), True),
                append_skill_materials=process_mats(
                    data.get("appendSkillMaterials", {}), True
                ),
            )
            db.session.add(new_servant)

        db.session.commit()
        print(f"[+] Saved {len(valid_servants)} servants to SQLite.")


if __name__ == "__main__":
    fetch_and_save_data()
