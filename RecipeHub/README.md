# RecipeHub

#### Video Demo: https://www.youtube.com/watch?v=v-dPzSHnuos

## Description

RecipeHub is a Flask-based web application developed as my final project for Harvard University's CS50x: Introduction to Computer Science. The purpose of the application is to provide users with a simple, modern, and organized platform where they can create, manage, search, and save their favorite recipes.

The idea behind RecipeHub was to combine the concepts learned throughout CS50 into a practical full-stack web application. The project integrates user authentication, database management, file uploads, PDF generation, responsive web design, and client-side interactivity. Rather than simply displaying recipes, the application allows users to build their own personal recipe collection while exploring recipes in an intuitive interface.

Users can register for an account, securely log in, add recipes with images, search recipes by title, mark recipes as favorites, rate recipes, and download them as PDF documents. Throughout the project, I focused on creating an interface that is both visually appealing and easy to use.

---

## Features

RecipeHub includes the following functionality:

- User registration and login with securely hashed passwords.
- Session-based authentication using Flask-Session.
- Add new recipes with uploaded images.
- Store recipe information in an SQLite database.
- Search recipes by title.
- View complete recipe details.
- Favorite and unfavorite recipes.
- Personal **My Recipes** page displaying recipes created by the logged-in user.
- Recipe ratings with average ratings displayed.
- Share recipes using the browser's sharing functionality or copy the recipe link.
- Download recipes as professionally formatted PDF documents.
- Responsive user interface using Bootstrap 5.

---

## Technologies Used

### Backend

- Python
- Flask
- SQLite
- CS50 SQL Library

### Frontend

- HTML
- CSS
- Bootstrap 5
- JavaScript
- Font Awesome

### Additional Libraries

- Flask-Session
- Werkzeug
- ReportLab
- WeasyPrint

---

## Project Structure

### app.py

This file contains the main Flask application. It defines all routes used throughout the website, including user registration, login, logout, recipe creation, searching, viewing recipes, managing favorites, submitting ratings, and downloading recipes as PDF files. It also contains the SQL queries used to communicate with the SQLite database.

### templates/

The templates folder contains all HTML pages rendered by Flask. These templates include the homepage, login page, registration page, recipe creation form, search results page, recipe details page, favorites page, and the user's personal recipe collection. Jinja templating is used to dynamically display recipe information stored in the database.

### static/

The static folder stores the application's CSS stylesheet, uploaded recipe images, icons, and any additional static resources required by the website. Uploaded images are saved inside the uploads folder and displayed whenever recipes are viewed.

### recipes.db

The SQLite database stores all application data, including user accounts, recipes, favorite recipes, and recipe ratings. Using a relational database made it easier to organize information efficiently while allowing different users to manage their own content independently.

### requirements.txt

This file lists the Python packages required to run the application so the project can easily be installed on another computer.

---

## Database Design

RecipeHub uses SQLite as its database management system.

The database stores four main types of information:

- User accounts
- Recipes
- Favorite recipes
- Recipe ratings

Each recipe includes information such as:

- Title
- Description
- Ingredients
- Instructions
- Preparation time
- Cooking time
- Servings
- Difficulty
- Category
- Uploaded image
- Creator

Separating recipes, favorites, and ratings into different tables simplifies database management while avoiding unnecessary duplication of data.

---

## Design Decisions

One of the biggest design decisions was creating a modern interface instead of using simple tables to display recipes. I chose large horizontal recipe cards because they provide more space for images and descriptions while making the website feel more similar to modern recipe platforms.

Bootstrap was used extensively to keep the interface responsive across different screen sizes while reducing the amount of custom CSS required. Font Awesome icons were added to improve usability by providing recognizable visual actions for features such as favorites, downloading, and sharing.

For PDF downloads, I chose to generate professionally formatted recipe documents so users could save recipes offline or print them easily. This feature adds practical value beyond simply viewing recipes in the browser.

Another important design decision was implementing secure authentication using hashed passwords instead of storing passwords directly in the database. Flask-Session was used to maintain user sessions securely throughout the application.

---

## Challenges

Developing RecipeHub involved combining many different concepts learned throughout CS50 into a single application. One challenge was connecting the frontend and backend so that information entered by users would be stored correctly in the database and displayed dynamically.

Another challenge was designing an attractive interface while keeping the website responsive on different screen sizes. Features such as favorites, ratings, image uploads, PDF generation, and searching each required careful integration between Flask, SQLite, HTML, CSS, and JavaScript.

Debugging database queries and ensuring that only authenticated users could access certain features also required careful testing throughout development.

---

## Future Improvements

If I continue developing RecipeHub, I would like to add several additional features, including:

- Advanced filtering by category and difficulty
- User profile pages
- Recipe editing history
- Nutritional information
- Recipe recommendations
- User comments and reviews
- Meal planning functionality

---

## Conclusion

RecipeHub demonstrates the knowledge and skills I gained throughout CS50 by combining backend development with frontend design into a complete web application. Building this project strengthened my understanding of Flask, SQLite, HTML, CSS, JavaScript, and responsive web design while also teaching me how different technologies work together in a full-stack application.

Overall, RecipeHub provides users with an easy and organized way to create, manage, search, and share recipes while offering a clean, modern, and user-friendly experience.
