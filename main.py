from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy

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
    face_url = db.Column(db.String(255))


html = """
<h1>FGO Servants</h1>
{% for servant in servants %}
<div style="margin-bottom: 10px;">
    <img src="{{ servant.face_url }}" width="50" style="vertical-align: middle;">
    <b>ID:{{ servant.servant_id }} | {{ servant.name }} (Class: {{ servant.class_name.capitalize() }})</b>
</div>
{% endfor %}
"""


@app.route("/")
def index():
    # วนลูปเอาข้อมูลมาต่อ String
    servants = Servant.query.all()
    return render_template_string(html, servants=servants)


if __name__ == "__main__":
    app.run(debug=True)
