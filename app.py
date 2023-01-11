import re
import calendar
import db as dbFunctions

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functions import login_required, current_year
from datetime import date
from operator import itemgetter

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/budget_monthly", methods=["GET", "POST"])
def budget_monthly():
    # List of categories that can be chosen
    categories = ['Income','-','Savings','-','Debt', 'Education', 'Entertainment', 'Fashion', 'Food', 'Health', 'Holidays', 'Housing', 'Insurance', 'Others', 'Pet', 'Taxes', 'Technology', 'Transport', 'Utilities']

    # List the available months for selection, and set current month to today
    months = [calendar.month_name[i] for i in range(1,13)]

    # Initialize an empty list and variable i, then iterate over each month to append each month and number to list
    monthCollection = []
    i = 1
    for month in months:
        monthCollection.append(month)
        monthCollection.append(i)
        i += 1

    # Get current year
    currentYear = current_year()

    # If POST-request is sent, month selected should be changed
    if request.method == "POST":
        monthSelected = request.form.get("monthSelected")
    else:
        monthSelected = calendar.month_name[date.today().month]

    monthNumber = monthCollection[(monthCollection.index(monthSelected)) + 1]
    monthNumber = str(monthNumber) # convert to string

    # Add 0 if number of month is less than 10
    if len(monthNumber) <= 1:
        monthNumber = "0" + monthNumber

    # This is part of the search query in the database
    searchDate = "%" + currentYear + "-" + monthNumber + "%"

    # Retrieve budget for user from database using specified year and month
    budget = dbFunctions.getBudgetH_date(session["user_id"],searchDate)

    # Set total amount to 0, if budget is already available, a new total will be calculated below
    totalAmount = 0
    # Place-holder in case the table is empty; hide the delete-button and set the budget to empty
    if len(budget) < 1:
        showDelBt = False
        budget = [("No data","No data","No data","No data","No data")]
    else:
        # Calculate the total amount stored in the budget_history-db for the selected period
        showDelBt = True
        for entry in budget:
            totalAmount += entry[2]

    # Return the budget template
    return render_template("budget_monthly.html",categories=categories,budget=budget,totalAmount=totalAmount,showDelBt=showDelBt,months=months,monthSelected=monthSelected,currentYear=currentYear)

@app.route("/budget_overview", methods=["GET", "POST"])
def budget():
    # Get current year for search in the database
    currentYear = current_year()

    # Retrieve data for current year from database for user
    budgetData = dbFunctions.getBudgetH_group(session["user_id"],"%" + currentYear + "%")

    # Calculate the total balance for the year from the data, and format it with a decimal
    totalBalance = "{:,}".format(sum([x[1] for x in budgetData]))

    # Remove Income and Savings from data so we only have the expenses left
    newBudgetData = [i for i in budgetData if i[0] != 'Income']
    newBudgetData = [i for i in newBudgetData if i[0] != 'Savings']

    # Calculate the total expenses for the year, convert them to positive number and format it with a decimal
    totalExpenses = "{:,}".format(sum([x[1] for x in newBudgetData]))

    # Get the highest category for expenses other than Income and Savings
    highestCategory = list((x, abs(i)) for x, i in newBudgetData)
    highestCategory = max(highestCategory,key=itemgetter(1))[0]

    # Create new dict and store the budget data in it, this will be used for the pie chart
    budgetPie = {'Category' : 'Amount'}
    tempBudget = dict((x, abs(y)) for x, y in budgetData)
    budgetPie.update(tempBudget)

    return render_template("budget_overview.html",budgetPie=budgetPie,currentYear=currentYear,totalBalance=totalBalance,totalExpenses=totalExpenses,highestCategory=highestCategory)

# Defines the function to input posts into the budget
@app.route("/inputbudget", methods=["POST"])
@login_required
def inputbudget():
    if request.method == "POST":
        # Get variables below for easier access
        amount = request.form.get("amount")
        description = request.form.get("description")

        # If amount or category is not provided, or if description is too long, just reload the page
        if not amount or request.form.get("category") == "-":
            flash('You have to provide amount and/or category.', 'errorFlash')
            return redirect("/budget")
        elif len(description) > 12:
            flash('Description is too long. Please provide less than 12 characters.', 'errorFlash')
            return redirect("/budget")

        # Clean amount-variable if it contains any non-digits
        if not amount.isdigit():
           amount = re.sub('\D', '', amount)

        # Add minus sign if it's not a Income, Saving or Investment
        if not request.form.get("category") in ("Income","Savings","Investmest"):
            amount = "-" + amount

        # Insert into budget_history-db and then redirect to /budget
        dbFunctions.insertBudgetH(int(session["user_id"]),request.form.get("category"),amount,description,date.today())
        return redirect("/budget_monthly")

# Defines the function to input posts into the budget
@app.route("/deletefrombudget", methods=["POST"])
@login_required
def deletefrombudget():
    if request.method == "POST":

        # Delete post from budget_history-db for user
        dbFunctions.deletefromBudgetH(int(session["user_id"]),int(request.form.get("delete")))
        return redirect("/budget_monthly")

# Simply renders the about.html template
@app.route("/about")
def about():
    return render_template("about.html")

# Simply renders the myaccount.html template
@app.route("/myaccount")
@login_required
def myaccount():
    return render_template("myaccount.html")

# Define login function
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # If request method is GET, simply return the login page
    if request.method == "GET":
        return render_template("login.html")

    # If request method is POST, we do more logic below
    if request.method == "POST":
         # Ensure username was submitted
        if not request.form.get("username"):
            flash('Username must be provided.', 'errorFlash')
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Password must be provided.', 'errorFlash')
            return render_template("login.html")

        # Query database for username
        else:
            user = dbFunctions.checkUser(request.form.get("username"))

            # Verify username and password
            if user == None or not check_password_hash(str(user[2]), request.form.get("password")):
                flash('Username or password is incorrect.', 'errorFlash')
                return render_template("login.html")
            elif user != None and check_password_hash(str(user[2]), request.form.get("password")):
                session["user_id"] = (str(user[0]))
                flash('You have successfully logged in.', 'infoFlash')
                return render_template("index.html")

# Define signup (registration)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    # Signup functions
    if request.method == "POST":

    # Ensure username was submitted
        if not request.form.get("username"):
            flash('Username must be provided.', 'errorFlash')
            return render_template("signup.html")

        # Ensure username doesn't exist
        elif dbFunctions.checkUser(request.form.get("username")):
            flash('Username already exists. Please select another username.', 'errorFlash')
            return render_template("signup.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Password must be provided.', 'errorFlash')
            return render_template("signup.html")

        # Ensure passwords match
        elif not request.form.get("password") == request.form.get("confirmpassword"):
            flash('Password must match.', 'errorFlash')
            return render_template("signup.html")

        # Ensure password has a minimum of 8 characters, and contains atleast one numeral and one capital letter
        elif len(request.form.get("password")) < 8:
            flash('Password must be atleast 8 characters.', 'errorFlash')
            return render_template("signup.html")
        elif not any(char.isdigit() for char in request.form.get("password")):
            flash('Password must contain atleast one numeral.', 'errorFlash')
            return render_template("signup.html")
        elif not any(char.isupper() for char in request.form.get("password")):
            flash('Password must contain atleast one uppcase character.', 'errorFlash')
            return render_template("signup.html")

        # Else, register user in database
        else:
            hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=16)
            dbFunctions.insertUser(request.form.get("username"),hash)
            flash('Successfully registered. Please login.', 'infoFlash')
            return redirect("/login")

# Define password reset functionality
@app.route("/resetpassword", methods=["GET", "POST"])
@login_required
def resetpassword():
    if request.method == "GET":
        return render_template("resetpassword.html")

    # Reset password function
    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("password"):
            flash('Password must be provided.', 'errorFlash')
            return render_template("resetpassword.html")

        # Ensure passwords match
        elif not request.form.get("password") == request.form.get("confirmpassword"):
            flash('Passwords must match.', 'errorFlash')
            return render_template("resetpassword.html")

        # Ensure password has a minimum of 8 characters, and contains atleast one numeral and one capital letter
        elif len(request.form.get("password")) < 8:
            flash('Password must be atleast 8 characters.', 'errorFlash')
            return render_template("resetpassword.html")
        elif not any(char.isdigit() for char in request.form.get("password")):
            flash('Password must contain atleast one numeral.', 'errorFlash')
            return render_template("resetpassword.html")
        elif not any(char.isupper() for char in request.form.get("password")):
            flash('Password must contain atleast one uppcase character.', 'errorFlash')
            return render_template("resetpassword.html")

        # Else, reset users password
        else:
            hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=16)
            dbFunctions.resetPassword(hash,int(session["user_id"]))
            flash('Successfully changed password.', 'infoFlash')
            return redirect("/myaccount")

@app.route("/deleteaccount", methods=["POST"])
@login_required
def deleteaccount():
    dbFunctions.deleteAccount(int(session["user_id"]))
    session.clear()
    flash('Your account and data was deleted.', 'infoFlash')
    return redirect("/")

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to about page
    flash('You have logged out.', 'infoFlash')
    return redirect("/")

# Simple error handling from flask
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404