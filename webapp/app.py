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


@app.route('/recipe/<recipe_id>', methods=['POST', 'GET'])
def recipeDetail(recipe_id):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    user =  db.users.find_one({'username': session["username"]})
    user_saved = user["saved"]
    if (recipe_id in user_saved):
        isSaved = True
    else:
        isSaved = False
    
    # render the edit template
    
    if request.method == 'POST':
        newcomment = request.form['description']
        temp = db.recipes.find({"_id":ObjectId(recipe_id)})[0]
        comments = temp['comments']
        comments.append({"username":session["username"], "comment":newcomment})
        db.recipes.update_one({"_id":ObjectId(recipe_id)},
                              {'$set':{"comments":comments}})
    recipe = db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('recipe-detail.html', r=recipe, isSaved=isSaved)


@app.route('/recipe/<recipe_id>/edit')
def recipeEdit(recipe_id):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    recipe = db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('editRecipe.html', recipe=recipe)


@app.route('/recipe/<recipe_id>/edit', methods=['POST'])
def EditRecipe(recipe_id):
    photo = request.files['image']
    filename = photo.filename
    title = request.form["title"]
    estimatedTime = request.form["estimatedTime"]
    numServings = request.form["numServings"]
    estimatedCost = request.form["estimatedCost"]
    difficultyLevel = request.form["difficultyLevel"]
    cuisine = request.form["cuisine"]
    description = request.form["description"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    nameOfUser = session['username']
    old = db.recipes.find({"_id":ObjectId(recipe_id)})[0]
    updated_recipe = {
        "user": nameOfUser,
        "title": title,
        "estimatedTime": estimatedTime,
        "numServings": numServings,
        "estimatedCost": estimatedCost,
        "difficultyLevel": difficultyLevel,
        "cuisine": cuisine,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "comments": old['comments']
    }

    if filename != "":
        updated_recipe["image"] = filename
        photo.save('./static/images/'+filename)

    db.recipes.update_one(
        {"_id": ObjectId(recipe_id)},  # match criteria
        {"$set": updated_recipe}
    )

    return redirect(url_for('myRecipes'))


@app.route('/recipe/<recipe_id>/delete')
def recipeDelete(recipe_id):
    """
    Route for GET requests to the edit page.
    Displays a form users can fill out to edit an existing record.
    """
    db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    return redirect(url_for('myRecipes'))


@app.route('/recipe-add', methods=['POST'])
def addRecipe():
    photo = request.files['image']
    filename = photo.filename
    photo.save('./static/images/'+filename)
    title = request.form["title"]
    estimatedTime = request.form["estimatedTime"]
    numServings = request.form["numServings"]
    estimatedCost = request.form["estimatedCost"]
    difficultyLevel = request.form["difficultyLevel"]
    cuisine = request.form["cuisine"]
    description = request.form["description"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    nameOfUser = session['username']
    new_recipe = {
        "user": nameOfUser,
        "image": filename,
        "title": title,
        "estimatedTime": estimatedTime,
        "numServings": numServings,
        "estimatedCost": estimatedCost,
        "difficultyLevel": difficultyLevel,
        "cuisine": cuisine,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "comments":[]
    }

    db.recipes.insert_one(new_recipe)
    return redirect(url_for('browse'))


@app.route('/my-recipes')
def myRecipes():
    """
    Route for the home page
    """
    recipes = db.recipes.find({"user": session['username']})
    # render the home template
    return render_template('myRecipes.html', recipes=recipes)


@app.route('/logout')
def logout():
    """
    Route for the home page
    """
    session.pop("username")
    return render_template('index.html')  # render the home template


@app.route('/saved-recipes')
def savedRecipes():
    """
    Route for the saved recipes
    """
    currUser = db.users.find({"username": session['username']})
    savedItems = currUser[0]['saved']

    print(savedItems)
    for rec in db.recipes.find({}):
        if (str(rec.get("_id")) in savedItems):
            # print("found")
            db.recipes.update_one({"_id": rec.get("_id")},
                                  {"$set": {"found": "1"}})
        else:
            # print("not found")
            db.recipes.update_one({"_id": rec.get("_id")},
                                  {"$set": {"found": "0"}})

    return render_template('savedRecipes.html', recipes=db.recipes.find({"found": "1"}))


@app.route('/saveRecipe', methods=['GET'])
def saveNew():
    if (request.args.get('recipe_id') == ""):
        print("none")
        return redirect(url_for("savedRecipes"))
    else:
        recipe_id = request.args.get('recipe_id')
        currUser = db.users.find({"username": session['username']})
        savedItems = currUser[0]['saved']
        
        if (str(recipe_id) not in savedItems):
            savedItems.append(recipe_id)
        else:
            savedItems.remove(recipe_id)

        db.users.update_one({"username": session['username']},
                            {"$set": {'saved': savedItems}})

        print(savedItems)
        for rec in db.recipes.find({}):
            if (str(rec.get("_id")) in savedItems):
                # print("found")
                db.recipes.update_one({"_id": rec.get("_id")},
                                      {"$set": {"found": "1"}})
            else:
                # print("not found")
                db.recipes.update_one({"_id": rec.get("_id")},
                                      {"$set": {"found": "0"}})

        return render_template('savedRecipes.html', recipes=db.recipes.find({"found": "1"}))


app.secret_key = 'some key that you will never guess'
if __name__ == "__main__":
    # use the PORT environment variable, or default to 5000
    PORT = os.getenv('PORT', 5000)
    # import logging
    # logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(port=PORT)
