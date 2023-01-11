from flask import redirect, session
from functools import wraps
from datetime import date

# Requires login, see: https://flask.palletsprojects.com/en/1.0.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Gets current year as string
def current_year():
    current_year = (date.today()).strftime("%Y")
    return current_year