from flask import Flask
import requests

app = Flask(__name__)


@app.route("/")
def show_servants():
    # ดึงข้อมูลจาก API
    url = "https://api.atlasacademy.io/export/NA/basic_servant.json"
    response = requests.get(url)
    all_servants = response.json()
    html = "<h1>FGO Servants</h1>"
    # วนลูปเอาข้อมูลมาต่อ String
    for servant in all_servants:
        name = servant["name"]
        fgo_class = servant["className"].capitalize()
        face_url = servant["face"]
        servant_id = servant["collectionNo"]
        html += f"""
        <div style="margin-bottom: 10px;">
            <img src="{face_url}" width="50" style="vertical-align: middle;">
            <b>{servant_id}. {name}</b> (Class: {fgo_class})
        </div>
        """
    return html


if __name__ == "__main__":
    app.run(debug=True)
