# Budget Made Simple
#### Video Demo:  https://www.youtube.com/watch?v=37s2nsm9p0o
#### Description:

***Budget Made Simple is my final project for CS50.*** Essentially, it is a Flask-application built using Python (Flask) and SQL (Sqlite3) as it's foundation, and HTML, CSS, a little bit of Jinja and JavaScript. Other than CSS is also incorporates Bootstrap. This decision was consciously made as it helped creating the frontend part of Budget Made Simple much faster, as Bootstrap provides several solutions out of the box.

The application allows a user to sign up, login and then manually add and delete their own entries to keep track of their budget. It has some simple functionality to show an overview of the budget stored in the database back to the user. It also allows them to change their password and delete their account if they want to.

## app.py, db.py, database.db and functions.py
- **app.py** contains all routes needed to make the website function. While some routes only take GET-requests (for about.html, index.html, myaccount.html), most routes also take POST-requests. While most functionality resides here, some functions have been placed in db.py and functions.py to declutter app.py somewhat. Most of the backend logic however still takes place in app.py directly under each route.

- **db.py** contains all the functions that are used to interact with the Sqlite3 database. It allows the user to register an account, change their password and delete their account in the users-table in database.db. There are also functions used to validate the users identity (username and password) and to ensure no one can register two accounts with the same username.
<br><br>Other functions interact with the budget_history-table, allowing the user to insert and delete entries and retrieve an overview of their budget either for the whole year (budget_overview.html) or each individual entry (budget_monthly.html).

- **functions.py** only contains two functions. One is the login_required-function (<i>for more information, see https://flask.palletsprojects.com/en/1.0.x/patterns/viewdecorators/</i>) which requires a user to be logged in to access certain routes in app.py. The second function, current_year, is used to get the current year in app.py.
<br><br>A future plan is to refactor functionality from app.py and instead place it in functions.py, to declutter app.py.

## Templates
- **404.html** is a simple, static page containing an image, an error message and a link back to index.html. It's called using Flasks app.errorhandler-route when you try to access a page that does not exist.

- **about.html** is a simple, static page containing information about the website itself and me. It's reachable regardless if you're signed in or not using a GET-request to the /about-route in app.y.

- **budget_monthly.html** is the most interactivate part of Budget Made Simple and is only reachable by registered users. Using both GET- and POST-requests it allows the user to input data:
    - A (pre-set) category
    - An optional description
    - Amount

    When the data is submitted, the data is written to the budget_history-table along with the date of when the data was submitted. budget_monthly.html also displays the data based on the chosen month (default view is the current month) for the current year. The data is displayed in a table using a Jinja for-loop. For each entry, there's also a Delete-button containing a JavaScript-confirmation where the user can remove each individual entry.

- **budget_overview.html** displays a yearly overview of all entries available for the user for the current year. It achieves this by using the data from database.db, converting it into a Python dictionary, and then using a Google Column Chart (<i>https://developers.google.com/chart/interactive/docs/gallery/columnchart</i>) in JavaScript to display the data as a column chart. I'd rather have the JavaScript-function from Google reside in static/scripts.js instead, but was unable to achieve it. Instead, the JavaScript-function is inline in budget_overview.html. There's also simple logic to display the current balance for the year, expenses (all categories except for 'Income' and 'Savings') and the category for which the person has the most expenses.

- **index.html** is the starting page and uses Jinja if/else-logic depending on if a user is logged in or not. If a user is not logged in, it uses three Bootstrap-cards to display information about why you should be using Budget Made Simple. If a user is logged in, it instead displays a Welcome-message and asks what the user wants to do, presenting two options; editing your budget or seeing your budget overview.

- **layout.html** is the basic template which is then extended in the other templates. In the head, it links Bootstrap as well as the styles.css file located in /static. It also link a Google-font that is used in the navbar, Googles Charts loader and scripts.js located in /static. When the body is loaded, it also calls the JavaScript-function showYear() which is located in /static/scripts.js and simply shows the current year in the footer.
<br><br>The navbar is based on Bootstrap, and uses Jinja if/else-logic to display different options depending on if the user is logged in or not. layout.html also incorporates a Flask flash-div right under the navbar. This is used to display flash messages (both errors which are red, and information which is green) to the user when needed.

- **login.html** is where the user can login. It uses a Bootstrap-form to login, and then validates user input in app.py. If all checks pass, the user gets logged in and the session is active.

- **myaccount.html** is only reachable when the user has logged in. It contains two POST-routes: /deleteaccount and /changepassword, allowing the user to delete their account if they want to, or change their password. Both routes interact with the database.

- **resetpassword.html** is reachable from myaccount.html using the /changepassword route, and interacts with the database to change the password for the currently logged in user.

- **signup.html** is a call-to-action page allowing the user to sign up. If all checks pass in the validation-phase in app.py, the user is registered in the users-table in database.db, and redirected to login.html where they can now sign in.

## /static

- **styles.css** is used for extra styling for some design choices that were easier handled directly using CSS, although the application predominantly uses the Bootstrap-framework.

- **scripts.js** contains only a single function, showYear(), that is used in the footer in layout.html to display the current year. This is loaded on every page.

- **There's** also static images in /static/img as well as a favicon.ico-file in /static.

## Future considerations

Due to time constraints and lack of knowledge, there are some design choices I'd like to improve in the future as I have more time and a better understanding of how it all goes together:

- I'd like to refactor a lot of the code in app.py and instead move it into functions.py or other .py-files, to get a better structure for the application and keep mostly the routes in app.py.

- Same goes for inline JavaScript, which I'd like to be moved to /static/scripts.js.

- Add more functionality, such as changing years for your data, have different categories in the column chart be in different colors etc.

- Nicer front-end design in general.

- An overall better structure, possibly using classes and blueprints.

## Ending notes

This was a very fun project and I learned a lot, especially working with databases and how to combine SQL, Python and JavaScript to present that data in a somewhat readable and nice way for the user. Although this was a small start and project, I'm looking forward to both doing new projects, but also developing Budget Made Simple further as it could be of use to me personally as well.