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
<head>
    <title>FGO Servants</title>
    <style>
        body {
            background-color: lightgray;
            font-family: Agency FB, sans-serif;
        }
        .grid { 
            display: flex; 
            flex-wrap: wrap;
            gap: 20px; 
        }
        .card { 
            background: white; 
            padding: 15px; 
            border-radius: 8px; 
            text-align: center; 
            width: 150px; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.5); 
        }
        .card img { 
            width: 80px; 
            height: 80px; 
            border-radius: 50%; 
        }
    </style>
</head>
<body>
    <h1>FGO Servants</h1>
    <div class="grid">
        {% for servant in servants %}
        <div class="card">
            <img src="{{ servant.face_url }}" alt="{{ servant.name }}">
            <p style="font-size: 18px; 
                font-weight: bold; 
                margin: 10px 0 5px;
                ">ID:{{ servant.servant_id }} | {{ servant.name }}
            </p>
            <p style="font-size: 16px; 
                color: gray; margin: 0;
                ">{{ servant.class_name.capitalize() }}
            </p>
        </div>
        {% endfor %}
    </div>
</body>
"""


@app.route("/")
def index():
    servants = Servant.query.all()
    return render_template_string(html, servants=servants)


if __name__ == "__main__":
    app.run(debug=True)
