from flask import Blueprint, redirect, url_for, render_template, request, session, flash
import json
from extentions import db, shopping_cart
from models.user import User

authenticate = Blueprint("authenticate", __name__)


@authenticate.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        session.permanent = True
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        session["email"] = email
        session["password"] = password

        found_user = User.query.filter_by(email=email).first()
        if found_user:
            flash("This email is already in use by an existing user, "
                  "please signin using a unique email / login using some other user in order to continue")
            return redirect(url_for("home"))
        else:
            user = User(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash("Signed in successfully!")
            return redirect(url_for("menu"))
    else:
        return render_template("signin.html")


@authenticate.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        password = request.form["password"]
        session["email"] = email
        session["password"] = password

        found_user = User.query.filter_by(email=email).first()
        if found_user:
            if password == found_user.password:
                shopping_cart.shopping_dict = json.loads(found_user.shopping_cart) if found_user.shopping_cart else {}
            else:
                flash("Password is incorrect! please try again.")
                return render_template("login.html")
        else:
            flash("User is not registered, please signin / login using some other user in order to continue.")
            return redirect(url_for("home"))

        flash("Logged in successfully!")
        return redirect(url_for("menu"))
    else:
        if "email" in session:
            flash("Already logged in.")
            return redirect(url_for("menu"))
        return render_template("login.html")


@authenticate.route("/logout")
def logout():
    if "email" in session:
        email = session.pop("email")
        session.pop("password")
        flash(f"{email} have been logged out!")
    return redirect(url_for("authenticate.login"))


@authenticate.route("/edit")
def edit_profile():
    pass
