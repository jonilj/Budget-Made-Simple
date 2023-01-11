import sqlite3

# Function to insert the username into the users-table
def insertUser(username,hash):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (str(username), str(hash)))
    con.commit()
    con.close()

# Function to reset users password
def resetPassword(hash,user_id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET hash = ? WHERE id = ?", (str(hash), user_id))
    con.commit()
    con.close()

# Function to verify that username is not already in use in the database
def checkUser(username):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	user = cur.execute("SELECT * FROM users WHERE username = ?", [username])
	return user.fetchone()

# Function to insert posts into the budget_history-table
def insertBudgetH(user_id,category,amount,description,date):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO budget_history (user_id, category, amount, description, date) VALUES (?, ?, ?, ?, ?)", (user_id, str(category), str(amount), str(description), date))
    con.commit()
    con.close()

# Function that retrieves the budget from the budget_history-table for the specific user ordered by date
def getBudgetH_date(user_id,searchDate):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    budget = cur.execute("SELECT id, category, amount, description, date FROM budget_history WHERE user_id = ? AND date LIKE ? ORDER BY date ASC", (user_id, searchDate))
    return budget.fetchall()

# Function that retrieves the budget from the budget_history-table for the specific user ordered by date
def getBudgetH_group(user_id,currentYear):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    budget = cur.execute("SELECT category, sum(amount) FROM budget_history WHERE user_id = ? AND date LIKE ? GROUP BY category", (user_id, currentYear))
    return budget.fetchall()

# Function that deletes the selected post from the table
def deletefromBudgetH(user_id,id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM budget_history WHERE user_id = ? AND id = ?", (user_id, id))
    con.commit()
    con.close()

# Function that deletes the selected post from the table
def deleteAccount(user_id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", [user_id])
    cur.execute("DELETE FROM budget_history WHERE user_id = ?", [user_id])
    con.commit()
    con.close()