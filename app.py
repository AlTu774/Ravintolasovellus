from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///ally"
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT name, area FROM restaurants ORDER BY views DESC;")
    views = result.fetchall()
    return render_template("index.html", views = views)

@app.route("/search_restaurant")
def search_restaurant():
    result = db.session.execute("SELECT area FROM restaurants GROUP BY area")
    areas = result.fetchall()
    amount = len(areas)
    return render_template("search_restaurant.html", areas = areas, amount = amount)

@app.route("/search1_results", methods = ["POST"])
def search1_results():
    s_term = request.form["search_term"]
    area = request.form["area"]
    result = db.session.execute("SELECT name FROM restaurants WHERE name LIKE :s_term AND area = :area", {"s_term":s_term+"%", "area":area})
    s_results = result.fetchall()
    return render_template("search1_results.html", s_results = s_results)