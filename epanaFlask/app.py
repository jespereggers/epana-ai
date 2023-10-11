from flask import Flask, flash, redirect, render_template, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import login_required, apology
import sqlite3

DATABASE = 'epanaFlask/epana'

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/', methods=["GET", "POST"])
@login_required
def index():  # put application's code here
    if request.method == "POST":
        return
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT email FROM users WHERE id = ?", (session["user_id"],))
        return render_template("index.html", email=cursor.fetchall()[0][0])


@app.route('/models', methods=["GET", "POST"])
@login_required
def models():
    if request.method == "POST":
        return
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT model_id FROM models WHERE owner_id = ?", (session["user_id"],))
        model_info = cursor.fetchall()
        print(model_info)
        return render_template("models.html", models=model_info)


@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        return
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT email, tier FROM users WHERE id = ?", (session["user_id"],))
        user_info = cursor.fetchall()[0]
        return render_template("account.html", email=user_info[0], tier=user_info[1])


@app.route('/login', methods=["GET", "POST"])
def login():
    db = get_db()
    cursor = db.cursor()
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        cursor.execute(
            "SELECT * FROM users WHERE email = ?", (request.form.get("email"),)
        )
        rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
                rows[0][2], request.form.get("password")
        ):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        flash("Login successful!", "success")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        db = get_db()
        cursor = db.cursor()
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not email:
            return apology("Please input a email", 400)
        if not password:
            return apology("Please input a Password", 400)
        if not confirmation:
            return apology("Please confirm your Password", 400)
        if not password == confirmation:
            return apology("Passwords do not match", 400)

        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, generate_password_hash(password)),
            )
            db.commit()
            print("User created")
        except sqlite3.IntegrityError:
            return apology("email already in use", 400)

        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        rows = cursor.fetchall()
        user_id = rows[0][0]
        print(user_id)
        session["user_id"] = user_id

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    app.run()
