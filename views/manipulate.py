from flask import Blueprint, redirect, url_for, render_template, request, session, flash
import json
from extentions import db, shopping_cart
from models.user import User

manipulate = Blueprint("manipulate", __name__)


@manipulate.route("/add", methods=["GET", "POST"])
def add_product():
    if "email" in session:
        if request.method == "POST":
            product_name = request.form.get("product_name")
            quantity = request.form.get("quantity")
            added = shopping_cart.add_product(product_name, int(quantity))
            if added:
                email = session["email"]
                found_user = User.query.filter_by(email=email).first()
                found_user.shopping_cart = json.dumps(shopping_cart.shopping_dict)
                db.session.commit()
                flash(f"{product_name} X {quantity} added to the shopping cart.")
                return redirect(url_for("menu"))
            else:
                flash("Product already appears in the shopping cart, you can update its quantity if necessary.")
                return redirect(url_for("update_product"))
        else:
            return render_template("add.html")
    else:
        flash("You are not logged in!")
        return redirect(url_for("authenticate.login"))


@manipulate.route("/update", methods=["GET", "POST"])
def update_product():
    if "email" in session:
        if request.method == "POST":
            product_name = request.form.get("product_name")
            quantity = request.form.get("quantity")
            total = shopping_cart.update_product(product_name, int(quantity))
            if total:
                email = session["email"]
                found_user = User.query.filter_by(email=email).first()
                found_user.shopping_cart = json.dumps(shopping_cart.shopping_dict)
                db.session.commit()
                flash(f"{product_name} X {total} in the shopping cart.")
                return redirect(url_for("menu"))
            else:
                flash("Product does not appear in the shopping cart, please add it first.")
                return redirect(url_for("add_product"))
        else:
            return render_template("update.html")
    else:
        flash("You are not logged in!")
        return redirect(url_for("authenticate.login"))


@manipulate.route("/remove", methods=["GET", "POST"])
def remove_product():
    if "email" in session:
        if request.method == "POST":
            product_name = request.form.get("product_name")
            quantity = request.form.get("quantity")
            removed = shopping_cart.remove_product(product_name, int(quantity))
            if removed:
                email = session["email"]
                found_user = User.query.filter_by(email=email).first()
                found_user.shopping_cart = json.dumps(shopping_cart.shopping_dict)
                db.session.commit()
                flash(f"{product_name} X {quantity} removed from the shopping cart.")
                return redirect(url_for("menu"))
            else:
                flash(f"Product {product_name} does not appear in the shopping cart!")
                return redirect(url_for("menu"))
        else:
            return render_template("remove.html")
    else:
        flash("You are not logged in!")
        return redirect(url_for("authenticate.login"))
