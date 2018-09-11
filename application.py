#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys
from flask import Flask, flash, redirect, render_template, request, url_for
from shortlnk import shorter

# Configure application
app = Flask(__name__)

# Connect to SQLite database
try:
    conn = sqlite3.connect('links.db', check_same_thread=False)
    db = conn.cursor()
    db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='links'")
    result = db.fetchall()
    if not result:
        db.execute("CREATE TABLE links (URL, key)")
        conn.commit()
except sqlite3.Error as e:
    sys.stdout.write('Error connection to database: {}'.format(e))
    raise

home_URL = 'http://127.0.0.1:5000'

@app.route("/", methods=["GET", "POST"])
def short():
    """Call for make URL short"""
    try:
        conn = sqlite3.connect('links.db', check_same_thread=False)
        db = conn.cursor()
        db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='links'")
        result = db.fetchall()
        if not result:
            db.execute("CREATE TABLE links (URL, key)")
            conn.commit()

        # User reached route via POST (as by submitting a form via POST)
        if request.method == "POST":

            # Ensure URL was submitted
            if not request.form.get("long_url"):
                return apology("You should provide URL...", 403)

            # Query database for URL
            query = (request.form.get("long_url"),)
            db.execute("SELECT * FROM links WHERE URL = ?", query)
            result = db.fetchall()

            # Check if there is a key for this URL
            if result:
                key = result[0][1]

            # If no such URL in db - make a key for the URL and save it to db
            else:
                key = shorter(request.form.get("long_url"))
                print('Inputed URL={}\n key={}'.format(request.form.get("long_url"), key))
                query = (request.form.get("long_url"), key)
                db.execute("INSERT INTO links VALUES (?,?)", query)
                conn.commit()

            short_link = home_URL + '/query?key=' + key
            print('Short URL = {}'.format(short_link))

        # User reached route via GET (as by clicking a link or via redirect)
        else:
            return render_template("index.html")

        return render_template("result.html", short_link=short_link, URL=request.form.get("long_url"))

    except sqlite3.Error as e:
        sys.stdout.write('Error connection to database: {}'.format(e))
        raise
    finally:
        conn.close()


@app.route("/query", methods=["GET"])
def query():
    """Redirect user from short link to initial long URL"""

    # parse arguments from GET
    key = request.args['key']

    redirect_to = '/'
    query = (str(key), )
    # check if there is the key in db
    db.execute("SELECT * from links WHERE key=?", query)
    result = db.fetchall()

    if result:
        redirect_to = result[0][0]  #(URL, key)
    # if no - apology
    else:
        return apology("There is no long URL for such short one...", 403)

    # Redirect user to login form
    return redirect(redirect_to)


def apology(message, code=400):
    """Renders message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code


if __name__=='__main__':
    app.run()

#conn.close()

