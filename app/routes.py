from .forms import LoginForm, LogOutForm
from.db.db_connections import auth_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required
from .models import User
from app import csrf





main= Blueprint("main", __name__)
dadash_blueprint = Blueprint('dash_blueprint', __name__, url_prefix='/match-torque-analyzer')

@main.route("/")
def index():
    return redirect(url_for("main.login"))


@main.route("/login", methods=["GET", "POST"])
def login():
    loginform= LoginForm()

    if loginform.validate_on_submit():
        username= loginform.username.data
        password= loginform.password.data

        user_id= auth_user(username, password)

        if user_id is not None:
            user= User(user_id, username)
            login_user(user)

            return redirect(url_for("dash_blueprint.index"))

        else:
            flash("Wrong username or password", "danger")
            return redirect(url_for("main.login"))
    
    return render_template("login.html", login_form=loginform)




@main.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    

    logout_user()
    return redirect(url_for("main.login"))


