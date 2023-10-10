from flask import Flask, flash, redirect, render_template, request, session
from helpers import login_required

app = Flask(__name__)



#db = SQLAlchemy(app)


@app.route('/', methods=["GET", "POST"])
# @login_required
def index():  # put application's code here
    if request.method == "POST":
        return render_template("index.html")
    else:
        return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run()
