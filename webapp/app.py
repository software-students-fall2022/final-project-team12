from operator import truediv
from flask import Flask, render_template, request, redirect, url_for, make_response, session
from dotenv import load_dotenv
import os
import pymongo
import datetime
from bson.objectid import ObjectId
import sys
import base64
from io import BytesIO
from werkzeug.utils import secure_filename
# from flask_uploads import UploadSet, configure_uploads, IMAGES
# instantiate the app

# UPLOAD_FOLDER = os.path("./images")

app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
load_dotenv()  # take environment variables from .env.

# turn on debugging if in development modeflas
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True  # debug mnode

cxn = pymongo.MongoClient(
    "mongodb+srv://project5:project5@cluster0.2y3zidj.mongodb.net/?retryWrites=true&w=majority")
try:
    # verify the connection works by pinging the database
    # The ping command is cheap and does not require auth.
    cxn.admin.command('ping')
    # db = cxn[os.getenv('MONGO_DBNAME')] # store a reference to the database
    db = cxn["p5"]  # store a reference to the database
    # if we get here, the connection worked!
    print(' *', 'Connected to MongoDB!')
except Exception as e:
    # the ping command failed, so the connection is not available.
    print('', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
    print('Database connection error:', e)  # debug'


# set up the routes

# route for the home page
@app.route('/')
def home():
    """
    Route for the home page
    """
    return render_template('index.html')  # render the home template


@app.route("/login", methods=["POST", "GET"])
def login():
    """
        login with registered username
    """
    if request.method == "POST":
        global user_name
        user_name = request.form["username"]
        user_password = request.form["password"]

        x = db.users.find_one({'username': user_name})
        if x is not None:
            if x['password'] == user_password:
                session['username'] = user_name
                return redirect(url_for('browse'))
            else:
                return render_template("login.html", message="Wrong Password")
        else:
            return render_template("login.html", message="Invalid Username")
    else:
        return render_template("login.html", message="")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user_name = request.form["username"]
        user_password = request.form["password"]

        # Checking Validation
        if len(user_name) == 0:
            return render_template("register.html", message="Please enter valid username")
        if len(user_password) == 0:
            return render_template("register.html", message="Please enter valid password")

        if db.users.count_documents({'username': user_name}) == 0:
            new_user = {
                'username': user_name,
                'password': user_password,
                'saved': []
            }
            db.users.insert_one(new_user)
            return redirect(url_for('login'))
        else:
            return render_template("register.html", message="User account already exists")
    else:
        return render_template("register.html")


@app.route('/browse')
def browse():
    """
    Route for the home page
    """
    recipes = db.recipes.find({})
    # render the home template
    return render_template('browse.html', recipes=recipes)


@app.route('/recipe-add')
def recipeAdd():
    """
    Route for the home page
    """
    return render_template('addRecipe.html')  # render the home template