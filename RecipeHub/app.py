from flask import Flask, render_template, redirect, request, session, make_response, abort
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import os
from werkzeug.utils import secure_filename

from io import BytesIO
from flask import send_file

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from weasyprint import HTML

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///recipes.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST", "GET"])
def search():
    user_id = session.get("user_id")
    q = request.form.get("q") if request.method == "POST" else request.args.get("q")

    if not q:
        return redirect("/")

    recipes = db.execute("SELECT * FROM recipes WHERE title LIKE ?", "%" + q + "%")

    # Get set of recipe IDs favorited by current user
    fav_ids = set()
    if user_id:
        favs = db.execute("SELECT recipe_id FROM favorites WHERE user_id = ?", user_id)
        fav_ids = {row["recipe_id"] for row in favs}

    # Attach is_favorite boolean to each recipe
    for recipe in recipes:
        recipe["is_favorite"] = recipe["id"] in fav_ids

    return render_template("search.html", recipes=recipes)
@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "GET":
        return render_template("add_recipe.html")
    image = request.files.get("image")

    filename = None

    if image and image.filename:
        filename = secure_filename(image.filename)

        image.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))

    db.execute("""
        INSERT INTO recipes
        (user_id, title, description, ingredients, instructions,image,
        prep_time, cook_time, servings, difficulty, category)

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    """,
    session["user_id"],
    request.form.get("title"),
    request.form.get("description"),
    request.form.get("ingredients"),
    request.form.get("instructions"),
    filename,
    request.form.get("prep_time"),
    request.form.get("cook_time"),
    request.form.get("servings"),
    request.form.get("difficulty"),
    request.form.get("category")
    )

    return redirect("/")

@app.route("/myrecipes")
def myRecipes():
    recipes = db.execute("SELECT * FROM recipes WHERE user_id = ?",session["user_id"])
    return render_template("my_recipes.html",recipes = recipes)

@app.route("/login", methods = ["POST","GET"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("errors.html",message = "Please enter a username",back = "/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("errors.html",message = "Please enter a password",back = "/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("errors.html",message = "Incorrect password",back = "/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return render_template("errors.html",message = "Must enter username",back = "/register")
        password = request.form.get("password")
        if not password:
            return render_template("errors.html", message = "Must enter password",back = "/register")
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return render_template("errors.html",message = "Confirm password",back = "/register" )
        if password != confirmation:
            return render_template("errors.html",message = "The passwords do not match",back = "/register")
        hash = generate_password_hash(password)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 0:
            return render_template("errors.html", message="Username already exists",back = "/register")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",username,hash)

        ids = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = ids[0]["id"]

        return redirect("/")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")

@app.route("/recipe/<int:id>")
def recipe(id):

    # Ensure user is logged in
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    # Get recipe
    recipe_data = db.execute(
        "SELECT * FROM recipes WHERE id = ?",
        id
    )

    if len(recipe_data) != 1:
        return redirect("/myrecipes")

    # Check if recipe is favorited
    fav_check = db.execute(
        "SELECT 1 FROM favorites WHERE user_id = ? AND recipe_id = ?",
        user_id,
        id
    )

    is_favorite = len(fav_check) > 0

    # Get average rating
    average = db.execute(
        """
        SELECT
            AVG(rating) AS avg_rating,
            COUNT(*) AS total
        FROM ratings
        WHERE recipe_id = ?
        """,
        id
    )

    # Get this user's rating
    my_rating = db.execute(
        """
        SELECT rating
        FROM ratings
        WHERE recipe_id = ?
        AND user_id = ?
        """,
        id,
        user_id
    )

    return render_template(
        "recipe.html",
        recipe=recipe_data[0],
        is_favorite=is_favorite,
        average=average[0],
        my_rating=my_rating
    )

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    recipe = db.execute(
        "SELECT * FROM recipes WHERE id = ? AND user_id = ?",
        id,
        session["user_id"]
    )

    if len(recipe) != 1:
        return redirect("/myrecipes")

    if request.method == "GET":
        return render_template(
            "edit_recipe.html",
            recipe=recipe[0]
        )

    image = request.files.get("image")

    filename = recipe[0]["image"]

    if image and image.filename:
        filename = secure_filename(image.filename)

        image.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

    db.execute("""
        UPDATE recipes

        SET
            title = ?,
            description = ?,
            ingredients = ?,
            instructions = ?,
            image = ?,
            prep_time = ?,
            cook_time = ?,
            servings = ?,
            difficulty = ?,
            category = ?

        WHERE id = ? AND user_id = ?
    """,

    request.form.get("title"),
    request.form.get("description"),
    request.form.get("ingredients"),
    request.form.get("instructions"),
    filename,
    request.form.get("prep_time"),
    request.form.get("cook_time"),
    request.form.get("servings"),
    request.form.get("difficulty"),
    request.form.get("category"),
    id,
    session["user_id"]
    )

    return redirect("/myrecipes")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):

    # Remove ratings first
    db.execute(
        "DELETE FROM ratings WHERE recipe_id = ?",
        id
    )

    # Remove favorites
    db.execute(
        "DELETE FROM favorites WHERE recipe_id = ?",
        id
    )

    # Delete the recipe
    db.execute(
        "DELETE FROM recipes WHERE id = ? AND user_id = ?",
        id,
        session["user_id"]
    )

    return redirect("/myrecipes")

@app.route("/favorite/<int:recipe_id>", methods=["POST"])
def toggle_favorite(recipe_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    # Toggle favorite in DB
    existing_fav = db.execute(
        "SELECT * FROM favorites WHERE user_id = ? AND recipe_id = ?",
        user_id, recipe_id
    )

    if existing_fav:
        db.execute("DELETE FROM favorites WHERE user_id = ? AND recipe_id = ?", user_id, recipe_id)
    else:
        db.execute("INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)", user_id, recipe_id)

    # Check if this click came from a search results page
    q = request.form.get("q")
    if q:
        # Redirect right back to search results with the exact same search query
        return redirect(f"/search?q={q}")

    return "", 204

@app.route("/favorites")
def favorites():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    # Fetch recipes favorited strictly by the current logged-in user
    print("Session user_id:", user_id)

    favorite_recipes = db.execute("""
    SELECT recipes.*
    FROM recipes
    JOIN favorites
    ON recipes.id = favorites.recipe_id
    WHERE favorites.user_id = ?
""", user_id)

    print("favorite_recipes:", favorite_recipes)

    return render_template("favorites.html", recipes=favorite_recipes)

@app.route("/rate/<int:id>", methods=["POST"])
def rate(id):

    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    rating = request.form.get("rating")

    if not rating:
        return redirect(f"/recipe/{id}")

    rating = int(rating)

    existing = db.execute(
        "SELECT * FROM ratings WHERE recipe_id = ? AND user_id = ?",
        id,
        user_id
    )

    if existing:

        db.execute(
            """
            UPDATE ratings
            SET rating = ?
            WHERE recipe_id = ? AND user_id = ?
            """,
            rating,
            id,
            user_id
        )

    else:

        db.execute(
            """
            INSERT INTO ratings (recipe_id, user_id, rating)
            VALUES (?, ?, ?)
            """,
            id,
            user_id,
            rating
        )

    average = db.execute(
        """
        SELECT
            AVG(rating) AS avg_rating,
            COUNT(*) AS total
        FROM ratings
        WHERE recipe_id = ?
        """,
        id
    )

    return {
    "average": f"{average[0]['avg_rating']:.1f}",
    "total": average[0]["total"]
    }

@app.route("/download/<int:recipe_id>")
def download(recipe_id):

    # 1. Fetch recipe
    recipes = db.execute(
        "SELECT * FROM recipes WHERE id = ?",
        recipe_id
    )

    if not recipes:
        abort(404)

    recipe = recipes[0]

    # 2. Fetch rating details
    ratings = db.execute(
        """
        SELECT AVG(rating) AS avg_rating, COUNT(rating) AS total
        FROM ratings
        WHERE recipe_id = ?
        """,
        recipe_id
    )

    average = ratings[0] if ratings else {
        "avg_rating": 0,
        "total": 0
    }

    # 3. Render PDF HTML template
    rendered_html = render_template(
        "recipe_pdf.html",
        recipe=recipe,
        average=average
    )

    # 4. Convert HTML to PDF
    pdf_bytes = HTML(
        string=rendered_html,
        base_url=request.url_root
    ).write_pdf()

    # 5. Send file download response
    response = make_response(pdf_bytes)

    response.headers["Content-Type"] = "application/pdf"

    safe_title = "".join(
        c for c in recipe["title"]
        if c.isalnum() or c in (" ", "_", "-")
    ).rstrip()

    response.headers["Content-Disposition"] = (
        f'attachment; filename="{safe_title}.pdf"'
    )

    return response
