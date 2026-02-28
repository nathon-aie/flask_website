from flask import Flask, render_template
from models import db, Servant
from utils import calculate_total_materials

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///servants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
@app.route("/class/all")
def index():
    servants = Servant.query.all()
    return render_template("index.html", servants=servants)


@app.route("/class/<class_name>")
def class_page(class_name):
    servants = Servant.query.filter_by(class_name=class_name).all()
    return render_template("index.html", servants=servants)


@app.route("/servant/<int:servant_id>/<path:name>")
def servant_detail(servant_id, name):
    servant = Servant.query.filter_by(servant_id=servant_id).first_or_404()

    # ใช้ฟังก์ชันจาก utils.py ช่วยจัดการข้อมูล Materials
    asc_mats, total_asc = calculate_total_materials(servant.ascension_materials)
    skl_mats, total_skl = calculate_total_materials(servant.skill_materials)
    apd_mats, total_apd = calculate_total_materials(servant.append_skill_materials)

    return render_template(
        "servant_detail.html",
        servant=servant,
        costume=servant.costumes_list,
        active_skills=servant.skills_list,
        append_skills=servant.append_skills_list,
        noble_phantasms=servant.nps_list,
        ascension_materials=asc_mats,
        total_ascension_materials=total_asc,
        skill_materials=skl_mats,
        total_skill_materials=total_skl,
        append_skill_materials=apd_mats,
        total_append_skill_materials=total_apd,
    )


if __name__ == "__main__":
    app.run(debug=True)
