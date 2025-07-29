from .forms import LoginForm, LogOutForm
from.db.db_connections import auth_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required
from .models import User
from app import csrf





main= Blueprint("main", __name__)
dash_blueprint = Blueprint('dash_blueprint', __name__, url_prefix='/dash')

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

            return redirect("/dash/")

        else:
            flash("Wrong username or password", "danger")
            return redirect(url_for("main.login"))
    
    return render_template("login.html", login_form=loginform)


# @main.route("/dash/match-analyzer", methods=["GET", "POST"])
# @login_required
# @csrf.exempt
# def match_analyzer():
#     return redirect("/dash/match-analyzer")
    


@main.route("/test", methods=["GET", "POST"])
@login_required
def test():
    logout_form= LogOutForm()
    return render_template("test.html", logout_form=logout_form)






@main.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    

    logout_user()
    return redirect(url_for("main.login"))


# ## API ROUTES

# @main.route("/api/upload", methods=["POST"])
# @login_required
# def api_upload():
#     return jsonify({
#         "status":"success",
#         "message":"Upload endpoint working",
#         "user_id": session.get("user_id")
#     })

# @main.route("/api/process", methods=["POST"])
# @login_required
# def api_process():
#     return jsonify({
#         "status":"success",
#         "message":"Process endpoint working",
#         "user_id": session.get("user_id")
#     })

# @main.route("/api/csrf-token", methods=["GET"])
# @login_required
# def get_csrf_token():
#     from flask_wtf.csrf import generate_csrf
#     return jsonify({
#         "csrf_token": generate_csrf()
#     })