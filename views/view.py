from flask import Blueprint, redirect, url_for, render_template, session, flash
from extentions import shopping_cart
from models.user import User

view = Blueprint("view", __name__)


@view.route("/cart")
def view_cart():
    if "email" in session:
        col_titles_list = ["#", "Product", "Quantity"]
        row_vals_lists = [[product, quantity] for product, quantity in shopping_cart.shopping_dict.items()]
        return render_template("cart.html", col_titles_list=col_titles_list,
                               row_vals_lists=row_vals_lists)
    else:
        flash("You are not logged in!")
        return redirect(url_for("authenticate.login"))


@view.route("/users")
def view_users():
    return render_template("users.html", users=User.query.all())
