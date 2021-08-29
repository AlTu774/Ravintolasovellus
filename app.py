from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT name, area, id FROM restaurants ORDER BY views DESC;")
    views = result.fetchall()
    if len(views) < 3:
        count = len(views)
    else:
        count = 3
    return render_template("index.html", views = views, count = count)

@app.route("/search_restaurant")
def search_restaurant():
    result = db.session.execute("SELECT area FROM restaurants GROUP BY area")
    areas = result.fetchall()
    amount = len(areas)
    return render_template("search_restaurant.html", areas = areas, amount = amount)

@app.route("/search1_results", methods = ["POST"])
def search1_results():
    s_term = request.form["search_term"]
    try:
        area = request.form["area"]
    except:
        result = db.session.execute("SELECT name FROM restaurants WHERE name LIKE :s_term", {"s_term":s_term+"%"})
        s_results = result.fetchall()   
        return render_template("search1_results.html", s_results = s_results)

    result = db.session.execute("SELECT name FROM restaurants WHERE name LIKE :s_term AND area = :area", {"s_term":s_term+"%", "area":area})
    s_results = result.fetchall()   
    return render_template("search1_results.html", s_results = s_results)

@app.route("/search_food")
def search_food():
    result = db.session.execute("SELECT area FROM restaurants GROUP BY area")
    areas = result.fetchall()
    amount = len(areas)
    return render_template("search_food.html", areas = areas, amount = amount)

@app.route("/search2_results", methods = ["POST"])
def search2_results():
    s_term = request.form["search_term"]
    try:
        area = request.form["area"]
    except:
        result = db.session.execute("SELECT food FROM menu WHERE food LIKE :s_term", {"s_term":s_term+"%"})
        s_results = result.fetchall()   
        return render_template("search1_results.html", s_results = s_results)
    
    area = request.form["area"]
    result = db.session.execute("SELECT M.food FROM menu M, restaurants R WHERE M.res_id = R.id AND M.food LIKE :s_term AND R.area = :area", {"s_term":s_term+"%", "area":area})
    s_results = result.fetchall()   
    return render_template("search1_results.html", s_results = s_results)

@app.route("/restaurant_page/<int:id>")
def restaurant_page(id):
    result = db.session.execute("SELECT name FROM restaurants WHERE id = :id", {"id":id})
    restaurant = result.fetchone()
    result = db.session.execute("SELECT food FROM menu WHERE res_id = :id", {"id":id})
    menu = result.fetchall()
    result = db.session.execute("SELECT R.stars, R.content, U.name FROM reviews R, users U WHERE R.user_id = U.id AND R.res_id = :id", {"id":id})
    reviews = result.fetchall()
    result = db.session.execute("SELECT SUM(stars)/COUNT(*) FROM reviews WHERE res_id = :id", {"id":id})
    average = result.fetchone()
    return render_template("restaurant_page.html", restaurant = restaurant, menu = menu, reviews = reviews, average = average) 

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_check", methods=["POST"])
def login_check():
    username = request.form["username"]
    password = request.form["password"]
    result = db.session.execute("SELECT id, password FROM users WHERE name = :username", {"username":username})
    user = result.fetchone()
    if not user:
        return redirect("/login_failed")
    else:
        hash_value = user.password
        check = check_password_hash(hash_value, password)
        if check:
            session["username"] = username
            return redirect("/")
        else:
            return redirect("/login_failed")

@app.route("/login_failed")
def login_failed():
    return render_template("login_failed.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/signin_failed")
def signin_failed():
    return render_template("signin_failed.html")

@app.route("/signin_check", methods=["POST"])
def signin_check():
    username = request.form["username"]
    password = request.form["password"]
    result = db.session.execute("SELECT name FROM users")
    names = result.fetchall()
    for name in names:
        if username == name[0]:
            return redirect("/signin_failed")
        
    hash_value = generate_password_hash(password)
    sql = db.session.execute("INSERT INTO users (name, password) VALUES (:username, :hash_value)", {"username":username, "hash_value":hash_value})
    db.session.commit()
    session["username"] = username
    return redirect ("/")

        


