import sqlite3 as sql
import time
import random
from werkzeug.security import generate_password_hash, check_password_hash


def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    hash = generate_password_hash(password)
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hash, DoB),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(f'SELECT * FROM users WHERE username = ?', (username,))
    user = con.execute("SELECT * FROM users WHERE username = ? COLLATE NOCASE", (username,)).fetchone()
    if cur.fetchone() == None:
        con.close()
        return False
    else:
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open('visitor_log.txt', 'r') as file:
            number = int(file.read().strip())
            number += 1
        with open('visitor_log.txt', 'w') as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if check_password_hash(user[2], password):
            con.close()
            return True
        else:
            return False


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
