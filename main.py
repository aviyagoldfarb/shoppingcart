from flask import Flask, redirect, url_for, render_template, session, flash

from settings import SECRET_KEY, PERMANENT_SESSION_LIFETIME, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

from extentions import db, shopping_cart

from views.authenticate import authenticate
from views.manipulate import manipulate
from views.view import view

app = Flask(__name__)

app.secret_key = SECRET_KEY
app.permanent_session_lifetime = PERMANENT_SESSION_LIFETIME

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

app.register_blueprint(authenticate)
app.register_blueprint(manipulate)
app.register_blueprint(view)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/menu")
def menu():
    if "email" in session:
        email = session["email"]
        products_num = shopping_cart.get_products_num()
        return render_template("menu.html", user=email, products_num=products_num)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # app.run(host="0.0.0.0")
    app.run()
