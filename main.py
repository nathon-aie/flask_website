from flask import Flask, render_template
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


@app.route("/")
def index():
    servants = Servant.query.all()
    return render_template("index.html", servants=servants)


@app.route("/saber")
def saber_page():
    saber_servants = Servant.query.filter_by(class_name="saber").all()
    return render_template("index.html", servants=saber_servants)


if __name__ == "__main__":
    app.run(debug=True)
