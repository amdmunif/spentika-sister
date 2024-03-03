import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from datetime import datetime

# Configuration application
app = Flask(__name__)

# Configuration session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure response aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Landing Page Of This Website"""
    artikel = "Artikel"
    pengumuman = "Pengumuman"
    article = db.execute("SELECT * FROM article WHERE type = ? LIMIT 9", artikel)
    pengumuman = db.execute("SELECT * FROM article WHERE type = ? LIMIT 9", pengumuman)
    # Return user to go to first page
    return render_template("index.html", article=article, pengumuman=pengumuman)

@app.route("/profile")
def profile():
    """Landing Page Of This Website"""
    # Return user to go to profile page
    return render_template("profile.html")

@app.route("/activity")
def activity():
    """Landing Page Of This Website"""
    # Return user to go to activity page
    return render_template("activity.html")

@app.route("/teacher")
def teacher():
    """Landing Page Of This Website"""
    # Return user to go to teachers page
    return render_template("teacher.html")

@app.route("/contactUs", methods=["GET", "POST"])
def contactUs():
    """Contact Us Page Of This Website"""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        title = request.form.get("title")
        message = request.form.get("message")
        status = "Need Review"
        db.execute("INSERT INTO feedback (name, email, title, message, status) VALUES (?, ?, ?, ?, ?)", name, email, title, message, status)
        # Success message
        flash("Congratulation! Your feedback successfully submit!")
        # Return user to go to Contact Us page
        return render_template("contactus.html")
    else:
        return render_template("contactus.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # When method POST, check the email and password
    if request.method == "POST":

        # Difine with variables for name input
        name = request.form.get("name")

        # Difine with variables for email input
        email = request.form.get("email")

        # Difine with variables for password input
        password = request.form.get("password")

        # Difine with variables for confirmation password input
        confirmation = request.form.get("confirmation")

        if email == "" or password == "" or confirmation == "":
            return apology("Check your input form", 400)

        # Check the password with confirmation password
        if password != confirmation:
            return apology("Wrong confirmation password", 400)

        # Check the email from database
        if db.execute("SELECT * FROM teacher WHERE email = :email", email=email):
            return apology("Email already exist", 400)

        # Generate password hash with function from helpers
        password = generate_password_hash(password)

        # Default value of role
        role = "Teacher"

        # Insert data into SQL database
        db.execute("INSERT INTO teacher (name, email, password, role) VALUES (?, ?, ?, ?)", name, email, password, role)

        new_uid = db.execute("SELECT LAST_INSERT_ROWID() AS id")[0]["id"]

        # Remember which user has logged in
        session["user_id"] = new_uid

        # Welcome message
        flash("Welcome! You have successfully registered!")

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            flash("Warning! You must provide email!")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Warning! You must provide password!")
            return render_template("login.html")

        # Query database for email
        rows = db.execute("SELECT * FROM teacher WHERE email = ?", request.form.get("email"))

        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Warning! Invalid email and/or password!")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Welcome message
        flash("Welcome! Enjoy your day!")

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/home")
@login_required
def home():
    """Show Page for Teacher"""
    user_id = session["user_id"]
    teacher = db.execute("SELECT * FROM teacher WHERE id = ?", user_id)
    return render_template("teacher/index.html", teacher=teacher)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/pengumuman")
@login_required
def pengumuman():
    user_id = session["user_id"]
    type = "Pengumuman"
    pengumuman = db.execute("SELECT * FROM article WHERE type = ? AND user_id = ?", type, user_id)
    teacher = db.execute("SELECT * FROM teacher WHERE id = ?", user_id)
    return render_template("teacher/anouncement.html", pengumuman=pengumuman, teacher=teacher)

@app.route("/article")
@login_required
def article():
    user_id = session["user_id"]
    type = "Artikel"
    article = db.execute("SELECT * FROM article WHERE type = ? AND user_id = ?", type, user_id)
    teacher = db.execute("SELECT * FROM teacher WHERE id = ?", user_id)
    return render_template("teacher/article.html", article=article, teacher=teacher)

@app.route("/addArticle")
@login_required
def addArticle():
    user_id = session["user_id"]
    teacher = db.execute("SELECT * FROM teacher WHERE id = ?", user_id)
    return render_template("teacher/articleAdd.html", teacher=teacher)

@app.route("/saveArticle", methods=["GET", "POST"])
@login_required
def saveArticle():
    user_id = session["user_id"]
    teacher = db.execute("SELECT * FROM teacher WHERE id = ?", user_id)

    if request.method == "POST":
        title = request.form.get("title")
        type = request.form.get("type")
        content = request.form.get("content")
        status = "Need Review"
        time = datetime.now().isoformat()

        db.execute("INSERT INTO article (title, type, content, status, time, user_id) VALUES (?, ?, ?, ?, ?, ?)", title, type, content, status, time, user_id)
        flash("Congratulation! Your article successfully create!")
        return redirect("/article")
    else:
        return render_template("teacher/articleAdd.html", teacher=teacher)


@app.route("/feedbackList")
@login_required
def feedbackList():
    user_id = session["user_id"]
    feedback = db.execute("SELECT * FROM feedback")
    teacher = db.execute("SELECT * FROM teacher WHERE id = ?", user_id)
    return render_template("teacher/feedback.html", feedback=feedback, teacher=teacher)

@app.route("/users")
@login_required
def users():
    user_id = session["user_id"]
    users = db.execute("SELECT * FROM teacher")
    teacher = db.execute("SELECT * FROM teacher WHERE id = ?", user_id)
    return render_template("teacher/users.html", users=users, teacher=teacher)
