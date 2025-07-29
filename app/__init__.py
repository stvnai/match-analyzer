import os
from flask import Flask
from flask_login import current_user
from flask import redirect, request, url_for

from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from .models import User
from .db.db_connections import get_user_by_id

from dash import Dash, dcc
from dash_app.layout import main_container
from dash_app.callbacks.update_data_callback import update_data_app
from dash_app.callbacks.initial_dataload_callback import initial_load
from dash_app.callbacks.logout_callback import log_out


load_dotenv()



token= os.getenv("SECRET_TOKEN")
login_manager = LoginManager()

csrf = CSRFProtect()

def create_flask_app():
    app = Flask(__name__)
    app.secret_key = token
    login_manager.init_app(app)
    csrf.init_app(app)

    from .routes import main
    app.register_blueprint(main)
    csrf._exempt_views.add('dash.dash.dispatch')
    



    @login_manager.user_loader
    def load_user(user_id):
        user_data= get_user_by_id(user_id)
        return User(user_data[0], user_data[1])
    
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @app.before_request
    def restrict_dash():
        if request.path.startswith("/dash") and not current_user.is_authenticated:
            return redirect(url_for("main.login"))

    return app


#DASH APP

def create_dash_app(flask_app_server):

    assets_path = r"H:\AI-Projects\match-analizer\dash_app\assets"

    dash_app= Dash(
        name="MatchAnalyzer",
        server=flask_app_server,
        suppress_callback_exceptions=True,
        assets_folder=assets_path,
        url_base_pathname='/dash/'
    )
    
    dash_app.title= "Match Analyzer"





    dash_app.layout= main_container

    update_data_app(dash_app)
    initial_load(dash_app)
    log_out(dash_app)

    
    return dash_app

