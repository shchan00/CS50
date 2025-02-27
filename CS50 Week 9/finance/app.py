import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute(
        "SELECT * FROM users WHERE id = ?", session["user_id"]
    )
    username = rows[0]["username"]
    cash = rows[0]["cash"]
    transections = db.execute(
        "SELECT symbol, SUM(shares) as this_shares FROM transections WHERE username = ? GROUP BY symbol", username)
    sum = 0
    index_info = []
    for i in transections:
        this_symbol = i["symbol"]
        this_price = lookup(this_symbol)["price"]
        this_total = this_price * i["this_shares"]
        sum += this_total
        index_info.append({"symbol": this_symbol, "shares": i["this_shares"], "price": usd(
            this_price), "total": usd(this_total)})
    totalsum = cash + sum
    return render_template("index.html", transections=index_info, cash=usd(cash), totalsum=usd(totalsum))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")
        else:
            stock = lookup(symbol)
            if not stock:
                return apology("invalid symbol")
        shares = request.form.get("shares")
        if not shares:
            return apology("missing shares")
        if (not shares.isdigit()):
            return apology("invalid shares")
        shares = int(shares)
        if shares < 1:
            return apology("invalid shares")
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"]
        )
        username = rows[0]["username"]
        cash = rows[0]["cash"]
        price = stock["price"]
        if not username:
            return apology("Cannot validate user")
        if not cash:
            return apology("Cannot find balance")
        cost = shares * stock["price"]
        if cost > cash:
            return apology("not enough cash")
        remaining = cash - cost
        db.execute("INSERT INTO transections (username, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   username, symbol, shares, price)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", remaining, session["user_id"])
        flash("bought!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute(
        "SELECT * FROM users WHERE id = ?", session["user_id"]
    )
    username = rows[0]["username"]
    transections = db.execute(
        "SELECT symbol, shares, price, Timestamp FROM transections WHERE username = ?", username)
    for i in transections:
        i["price"] = usd(i["price"])
    return render_template("history.html", transections=transections)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")
        else:
            stock = lookup(symbol)
            if not stock:
                return apology("invalid symbol")
            stock["price"] = usd(stock["price"])
            return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or not confirmation:
            return apology("Missing username/password")
        elif password != confirmation:
            return apology("Passwords don't match")
        else:
            password = generate_password_hash(password)
            try:
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)
                rows = db.execute(
                    "SELECT id FROM users WHERE username = ? AND hash = ?", username, password)
                if len(rows) == 1:
                    session["user_id"] = rows[0]["id"]
                flash("Registered!")
                return redirect("/")
            except ValueError:
                return apology("User Already Exists")


@app.route("/change", methods=["GET", "POST"])
def change():
    """Register user"""
    if request.method == "GET":
        return render_template("change.html")
    else:
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation:
            return apology("Missing password")
        elif password != confirmation:
            return apology("Passwords don't match")
        current_password = db.execute(
            "SELECT hash FROM users WHERE id = ?", session["user_id"])[0]["hash"]
        if check_password_hash(current_password, password):
            return apology("New password is same as the old one")
        else:
            password = generate_password_hash(password)
            db.execute("UPDATE users SET hash = ? WHERE id = ?", password, session["user_id"])
            flash("password changed!")
            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    rows = db.execute(
        "SELECT * FROM users WHERE id = ?", session["user_id"]
    )
    username = rows[0]["username"]
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")
        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol")
        shares = request.form.get("shares")
        if not shares:
            return apology("missing shares")
        if (not shares.isdigit()):
            return apology("invalid shares")
        shares = int(shares)
        available = db.execute(
            "SELECT SUM(shares) as this_shares FROM transections WHERE username = ? AND symbol = ? GROUP BY symbol", username, symbol)
        available = int(available[0]["this_shares"])
        if shares < 1:
            return apology("invalid shares")
        if shares > available:
            return apology("too many shares")
        cash = rows[0]["cash"]
        totalcash = cash + stock["price"] * shares
        shares = -shares
        db.execute("UPDATE users SET cash = ? WHERE id = ?", totalcash, session["user_id"])
        db.execute("INSERT INTO transections (username, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   username, symbol, shares, stock["price"])
        flash("Sold!")
        return redirect("/")
    else:
        symbols = db.execute(
            "SELECT DISTINCT symbol FROM transections WHERE username = ?", username)
        return render_template("sell.html", available_symbols=symbols)
