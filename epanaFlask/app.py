# naming convention for saved files: output_<file_id>.jsonl for the output file,
# verification_<file_id>.jsonl for the verification file and upload_<file_id>.txt for the uploaded file
import datetime

from flask import Flask, flash, redirect, render_template, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import login_required, apology
import sqlite3

from chat_converter import chat_to_jsonl
from finetuning import start_finetuning_job

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
def index():
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
        # TODO: model database should probably hold the original filename to make it easier to identify the model
        cursor.execute("SELECT model_id FROM models WHERE owner_id = (?)", (session["user_id"],))
        model_info = cursor.fetchall()
        cursor.execute("SELECT name, date FROM input_files WHERE owner_id = (?)", (session["user_id"],))
        file_info = cursor.fetchall()
        # formate date to dd-mm-yyyy hh:mm
        formatted_file_info = [
            (file, datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M')) for file, date
            in file_info]
        return render_template("models.html", models=model_info, files=formatted_file_info)


@app.route('/create_model', methods=["GET", "POST"])
@login_required
def create_model():
    if request.method == "POST":
        return render_template("create_model.html")
    else:
        return render_template("create_model.html")


@app.route('/upload_file', methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":

        # FIXME: resubmitting the form will create a duplicate file; not sure how to fix; this might help:
        #  https://en.m.wikipedia.org/wiki/Post/Redirect/Get
        # connect to database
        db = get_db()
        cursor = db.cursor()

        # check if file was uploaded
        if not request.files['file']:
            return apology("Please input a file", 400)

        file = request.files['file']
        # craft filename
        cursor.execute("SELECT MAX(id) FROM input_files")
        max_input_id = cursor.fetchall()[0][0]
        if max_input_id is None:
            max_input_id = -1
        input_filename = "upload_" + str(max_input_id + 1) + ".txt"
        original_filename = file.filename
        # check if there is a row with the same filename in the database
        cursor.execute("SELECT * FROM input_files WHERE name LIKE ?", (original_filename + "%",))
        rows = cursor.fetchall()
        if len(rows) > 0:
            input_filename_db = original_filename + str(len(rows))
            print(str(len(rows)))
        else:
            input_filename_db = original_filename

        # save file to server
        filepath = "file_uploads/" + input_filename
        file.save(filepath)
        # add file to database
        cursor.execute("INSERT INTO input_files (owner_id, name) VALUES (?, ?)",
                       (session["user_id"], input_filename_db))

        # FIXME: make this more robust (e.g. make the output file name dependent on the amount of output files not
        #  input files in the database)
        # craft output filename
        output_name = "output_" + str(max_input_id + 1) + ".jsonl"
        output_path = "output_files/" + output_name
        verification_name = "verification_" + str(max_input_id + 1) + ".jsonl"
        verification_path = "output_files/" + verification_name
        # convert file to jsonl
        chat_to_jsonl(filepath, output_path, verification_path)
        # add files to database
        # TODO: add original filename to database instead of the generated one (DONE) or probably just delete the name
        #  column from the database cuz its not needed but idk, db structure might need some improvements
        cursor.execute("INSERT INTO output_files (owner_id, type, name) VALUES (?, ?, ?)",
                       (session["user_id"], "output", input_filename_db + "output"))
        cursor.execute("INSERT INTO output_files (owner_id, type, name) VALUES (?, ?, ?)",
                       (session["user_id"], "verification", input_filename_db + "verification"))
        flash("File: " + original_filename + " uploaded successfully", "success")
        db.commit()

        return redirect("/models")
    else:
        return render_template("upload_file.html")


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
        except sqlite3.IntegrityError:
            return apology("email already in use", 400)

        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        rows = cursor.fetchall()
        user_id = rows[0][0]
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
