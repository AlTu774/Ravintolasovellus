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
    try:
        result = db.session.execute("SELECT id FROM users WHERE name = :username", {"username":session["username"]})
        user_id = result.fetchone()
        return render_template("index.html", views = views, count = count, id = user_id)
    except:
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
        result = db.session.execute("SELECT name, id FROM restaurants WHERE name LIKE :s_term", {"s_term":s_term+"%"})
        s_results = result.fetchall()   
        return render_template("search1_results.html", s_results = s_results)

    result = db.session.execute("SELECT name, id FROM restaurants WHERE name LIKE :s_term AND area = :area", {"s_term":s_term+"%", "area":area})
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
        result = db.session.execute("SELECT M.food, R.name, R.id FROM menu M, restaurants R WHERE M.res_id = R.id AND M.food LIKE :s_term", {"s_term":s_term+"%"})
        s_results = result.fetchall()
        print(s_results)   
        return render_template("search2_results.html", s_results = s_results)
    
    area = request.form["area"]
    result = db.session.execute("SELECT M.food, R.name, R.id FROM menu M, restaurants R WHERE M.res_id = R.id AND M.food LIKE :s_term AND R.area = :area", {"s_term":s_term+"%", "area":area})
    s_results = result.fetchall()
    print(s_results)   
    return render_template("search2_results.html", s_results = s_results)

@app.route("/restaurant_page/<int:id>")
def restaurant_page(id):
    result = db.session.execute("SELECT views FROM restaurants WHERE id = :id", {"id":id})
    views = result.fetchone()[0]
    newviews = views + 1
    db.session.execute("UPDATE restaurants SET views = :views WHERE id = :id", {"views":newviews, "id":id})
    db.session.commit()
    result = db.session.execute("SELECT name FROM restaurants WHERE id = :id", {"id":id})
    restaurant = result.fetchone()
    result = db.session.execute("SELECT food FROM menu WHERE res_id = :id", {"id":id})
    menu = result.fetchall()
    result = db.session.execute("SELECT R.stars, R.content, U.name FROM reviews R, users U WHERE R.user_id = U.id AND R.res_id = :id ORDER BY R.id DESC", {"id":id})
    reviews = result.fetchall()
    result = db.session.execute("SELECT SUM(stars)/COUNT(*) FROM reviews WHERE res_id = :id", {"id":id})
    average = result.fetchone()
    try:
        sql = """
        SELECT
            R.id
        FROM
            reviews R, users U, restaurants RE
        WHERE
            R.user_id = U.id 
        AND
            R.res_id = RE.id
        AND
            U.name = :username
        AND
            RE.name = :restaurant
        """
        result = db.session.execute(sql, {"username":session["username"], "restaurant":restaurant[0]}) 
        r_id = result.fetchone()
        if not r_id:
            rated = False
        else:
            rated = True
        return render_template("restaurant_page.html", restaurant = restaurant, menu = menu, reviews = reviews, id = id, average = average, rated = rated)
    except:
        return render_template("restaurant_page.html", restaurant = restaurant, menu = menu, reviews = reviews, id=id,average = average)

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
    sql = db.session.execute("INSERT INTO users (name, password, address, paymethod, admin) VALUES (:username, :hash_value, ' ', ' ', False)", {"username":username, "hash_value":hash_value})
    db.session.commit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              ()
    session["username"] = username
    return redirect ("/")

@app.route("/review/<int:id>")
def review(id):
    result = db.session.execute("SELECT name FROM restaurants WHERE id = :id", {"id":id})
    restaurant = result.fetchone()
    result = db.session.execute("SELECT content FROM reviews WHERE user_id = :id", {"id":id})
    review = result.fetchone()
    if not review:
        rated = False
    else:
        rated = True
    return render_template("review.html", restaurant = restaurant, id = id, review = review)

@app.route("/review2/<int:id>", methods=["POST"])
def review2(id):
    review = request.form["review"]
    stars = request.form["stars"]
    result = db.session.execute("SELECT id FROM users WHERE name = :username", {"username": session["username"]})
    user_id = result.fetchone()
    result = db.session.execute("SELECT id FROM reviews WHERE user_id = :user_id AND res_id = :res_id", {"user_id":user_id[0], "res_id":id})
    review_id = result.fetchone()
    if not review_id:
        rated = False
    else:
        rated = True 
    if rated:
        result = db.session.execute("SELECT id FROM users WHERE name = :username", {"username":session["username"]})
        user_id = result.fetchone()
        sql = db.session.execute("UPDATE reviews SET content = :review, stars = :stars WHERE user_id = :user_id", {"user_id":user_id[0], "review":review, "stars":int(stars)})
        db.session.commit()
        return redirect("/restaurant_page/"+ str(id))
    else:
        sql = db.session.execute("INSERT INTO reviews (stars,content,user_id,res_id) VALUES (:stars, :review, :user_id, :res_id)", {"stars":int(stars), "review":review, "user_id":user_id[0], "res_id":id})
        db.session.commit()
        return redirect("/restaurant_page/"+str(id))

@app.route("/profile/<int:id>")
def profile(id):
    allow = False
    try:
        result = db.session.execute("SELECT id FROM users WHERE name = :username", {"username":session["username"]})
        session_id = result.fetchone()
        if session_id[0] == id:
            allow = True
        else:
            allow = False
    except:
        allow = False
    if not allow:
        return render_template("error.html")
    else:
        username = session["username"]
        result = db.session.execute("SELECT address, paymethod FROM users WHERE id = :id", {"id":id})
        info = result.fetchall()
        return render_template("profile.html", username = username, info = info)

@app.route("/menu/<int:id>")
def menu(id):
    result = db.session.execute("SELECT id, food, price FROM menu WHERE res_id = :id", {"id":id})
    items = result.fetchall()
    return render_template("menu.html", items = items, id = id)

@app.route("/order", methods=["POST"])
def order():
    amount = request.form.getlist("x")
    food_ids = request.form.getlist("food")
    res_id = request.form["res_id"]
    pricesum = 0
    foods = []
    for food_id in food_ids:
        result = db.session.execute("SELECT food, price FROM menu WHERE id = :id", {"id":food_id[0]})
        nameprice = result.fetchone()
        if amount[0] == '' :
            while amount[0] == '':
                amount.pop(0)
        pricesum = pricesum + int(amount[0])*nameprice[1]
        foods.append((nameprice[0],amount[0]))
        amount.pop(0)
    return render_template("order.html", foods = foods, pricesum = pricesum, res_id = res_id)

@app.route("/process_order", methods=["POST"])
def process_order():
    foods = request.form.getlist("food")
    pricesum = request.form["pricesum"]
    amounts = request.form.getlist("x")
    extras = request.form["extras"]
    address = request.form["address"]
    paymethod = request.form["paymethod"]
    res_id = request.form["res_id"]
    food_ids = []
    for food in foods:
        result = db.session.execute("SELECT id FROM menu WHERE res_id = :res_id AND food = :food", {"res_id":res_id, "food":food})
        food_ids.append(result.fetchone()[0])
    result = db.session.execute("SELECT id FROM users WHERE name = :username", {"username":session["username"]})
    user_id = result.fetchone()
    sql ="""
        INSERT INTO
            orders
            (pricesum, res_id, address, paymethod, extras, user_id)
        VALUES
            (:pricesum, :res_id, :address, :paymethod, :extras, :user_id)
        """
    result = db.session.execute(sql, {"pricesum":int(pricesum), "res_id":int(res_id), "address":address, "paymethod":paymethod, "extras":extras, "user_id":user_id[0]})
    db.session.commit()
    result = db.session.execute("SELECT MAX(id) FROM orders")
    order_id = result.fetchone()
    for x in amounts:
        sql ="""
            INSERT INTO
                orders_menu
                (food_id, x, order_id)
            VALUES
                (:food_id, :x, :order_id)
            """
        result = db.session.execute(sql, {"food_id":int(food_ids[0]), "x":int(x), "order_id":order_id[0]})
        db.session.commit()
        food_ids.pop(0)
    return render_template("order_done.html")
