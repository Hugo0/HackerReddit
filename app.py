import functools  # decorators

# webserver
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    Response,
    session,
    abort,
    flash,
    jsonify,
)
from flask_session import Session
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from sqlalchemy import create_engine  # DB
from sqlalchemy.orm import scoped_session, sessionmaker

# from flask_apscheduler import APScheduler  # for updating the data every 5 minutes
# import pytz

# import our own modules
import os

try:
    import secret
except ImportError:
    pass
from util import *

# logging is always good
import logging

logging.getLogger().addHandler(logging.StreamHandler())
rootLogger = logging.getLogger()
fileHandler = logging.FileHandler("logs/debug.log")
formatter = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s|%(message)s")
fileHandler.setFormatter(formatter)
rootLogger.addHandler(fileHandler)
rootLogger.setLevel("DEBUG")
rootLogger.info("-" * 40)


# Set up database

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# init flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# # setup scheduler
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()

# implementing login function
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"].lower()
        password = request.form["password"]

        if len(username) == 0 or len(password) == 0:
            return render_template("login.html")

        rootLogger.warning(f"Following user: {username} tried to login")
        stored_password_hash = db.execute(
            "SELECT pwd_hash FROM users WHERE username=:username",
            {"username": username},
        ).fetchone()[0]

        if check_password_hash(stored_password_hash, password):
            session["logged_in"] = True
            session["username"] = username
            rootLogger.info(f"login successfull for user {username}")
            return redirect(url_for("index"))

        # else redirect to login page
        else:
            rootLogger.warning("login unsuccessfull, redirecting to login")
            return render_template("login.html", message="Wrong username/password")


# implementing logout function
@app.route("/logout", methods=["GET", "POST"])
def logout():
    user = session["username"]
    rootLogger.warning(f"Following user: {user} is logging out")

    session["logged_in"] = False
    session.clear()

    return redirect(url_for("index"))


# wrapper function for login-required functionality
def login_required(f):
    @functools.wraps(f)  # preserves docstring of function
    def wrapped_function(*args, **kwargs):
        try:
            if session["logged_in"] is True:
                return f(**kwargs)
            else:
                return redirect(url_for("login"))
        except Exception as e:
            rootLogger.error(e)
            return handle_error(e)

        return f(*args, **kwargs)

    return wrapped_function


# route for users to register
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"].lower()
    password = request.form["password"]
    password_hash = generate_password_hash(password)
    email = request.form["email"]

    # check if username is already in database
    user_row = db.execute(
        "SELECT * FROM users WHERE username=:username", {"username": username}
    ).fetchone()
    if user_row is not None:
        message = """That username is already taken.
                     Please choose a different one"""
        return render_template("login.html", message=message, hide_login=True)
    else:
        # register the user
        db.execute(
            """INSERT INTO users (username, pwd_hash, email)
                   VALUES (:username, :password_hash, :email)""",
            {"username": username, "password_hash": password_hash, "email": email},
        )
        db.commit()

        session["logged_in"] = True
        session["username"] = username
        rootLogger.info(f"register successfull for user {username}")
        message = "Successfully registered!"
        return redirect("/")


# default route
@app.route("/")
def index():

    # get items to display
    if "username" in session:
        items = get_top(username=session["username"])
    else:
        items = get_top()

    return render_template("index.html", session=session, items=items)


# new posts
@app.route("/new")
def new():

    # get items to display
    if "username" in session:
        items = get_top(username=session["username"], new=True)
    else:
        items = get_top(new=True)

    return render_template("index.html", session=session, items=items)


# about info
@app.route("/about")
def about():

    return render_template("about.html", session=session)


# suggestions
@app.route("/suggestions")
def suggestions():

    return render_template("suggestions.html", session=session)


# legal stuff
@app.route("/legal")
def legal():

    return render_template("legal.html", session=session)


# errorhandler
@app.errorhandler(Exception)
def handle_error(e):
    rootLogger.error(e)
    return render_template("error.html", error=e)


# User Preferences
@app.route("/user/<string:username>", methods=["GET"])
@login_required
def user(username):

    user_row = db.execute(
        "SELECT * FROM users WHERE username=:username", {"username": username}
    ).fetchone()

    subreddits = db.execute(
        """SELECT DISTINCT subreddit FROM subreddits
            WHERE username=:username""",
        {"username": username},
    )

    # can only check data for one self
    if user_row["username"] == session["username"]:
        return render_template(
            "user.html", session=session, user=user_row, subreddits=subreddits
        )
    else:
        return redirect("/")


# subscribes a user to a subreddit
@app.route("/user/add_subreddit", methods=["POST"])
@login_required
def add_subreddit():
    username = request.form["username"]
    subreddit = request.form["subreddit"]

    # ensure has no spaces
    subreddit = subreddit.strip(" ")

    db.execute(
        """INSERT INTO subreddits (username, subreddit)
        VALUES (:username, :subreddit)""",
        {"username": username, "subreddit": subreddit},
    )
    db.commit()

    # if there are no posts from this subreddit in the db, add them
    item_row = db.execute(
        "SELECT * FROM items WHERE subreddit=:subreddit", {"subreddit": subreddit}
    ).fetchone()

    if item_row is None:
        update_subreddit(subreddit)

    return redirect("/user/" + username)


# unsubscribes a user from a subreddit
@app.route("/user/remove_subreddit", methods=["POST"])
@login_required
def remove_subreddit():
    username = request.form["username"]
    subreddit = request.form["subreddit"]

    # ensure has no spaces
    subreddit = subreddit.strip(" ")

    db.execute(
        """DELETE FROM subreddits WHERE
        username=:username and subreddit=:subreddit""",
        {"username": username, "subreddit": subreddit},
    )
    db.commit()

    return redirect("/user/" + username)


# start the flask application
if __name__ == "__main__":
    app.run(debug=False)
