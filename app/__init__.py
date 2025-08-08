import os
from pathlib import Path
from flask import Flask
from flask_login import current_user
from flask import redirect, request, url_for
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from .models import User
from .db.db_connections import get_user_by_id

from dash import Dash
from dash_app.match_layout import match_main_container
from dash_app.torque_layout import torque_main_container
from dash_app.main_layout import dash_main_container
from dash_app.callbacks.update_data_callback import update_data_app, torque_update_data_app
from dash_app.callbacks.redirect_callbacks import redirect_to_match_analyzer, redirect_to_torque_analyzer
from dash_app.callbacks.initial_dataload_callback import initial_load, torque_initial_load
from dash_app.callbacks.logout_callback import log_out, torque_log_out,  main_log_out


token= os.getenv("SECRET_TOKEN")
login_manager = LoginManager()
csrf = CSRFProtect()


def create_flask_app() -> Flask:

    """
    Description:
    -----
        Creates flask app with CSRF and Login Manager.

    :return Flask: flask app.
    
    """
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

def create_dash_match_analyzer(flask_app_server:Flask) -> Dash:

    """
    Description:
    -----
        Creates dash app into a flask server.

    :return Dash: dash app.
    
    """

    assets_path = Path(__file__).parent.parent / "dash_app" / "assets"

    dash_app= Dash(
        name="MatchAnalyzer",
        server=flask_app_server,
        suppress_callback_exceptions=True,
        assets_folder=assets_path,
        url_base_pathname="/dash/match-analyzer/"
    )
    
    dash_app.title= "Match Analyzer"

    dash_app.layout= match_main_container

    update_data_app(dash_app)
    initial_load(dash_app)
    log_out(dash_app)

    
    return dash_app

##### TORQUE ANALYZER #####

def create_dash_torque_analyzer(flask_app_server:Flask) -> Dash:

    """
    Description:
    -----
        Creates dash app into a flask server.

    :return Dash: dash app.
    
    """

    assets_path = Path(__file__).parent.parent / "dash_app" / "assets"

    dash_app= Dash(
        name="MatchAnalyzer",
        server=flask_app_server,
        suppress_callback_exceptions=True,
        assets_folder=assets_path,
        url_base_pathname="/dash/torque-analyzer/"
    )
    
    dash_app.title= "Torque Analyzer"

    dash_app.layout= torque_main_container

    torque_initial_load(dash_app)
    torque_update_data_app(dash_app)
    torque_log_out(dash_app)

    
    return dash_app

def create_dash_main(flask_app_server:Flask) -> Dash:

    """
    Description:
    -----
        Creates dash app into a flask server.

    :return Dash: dash app.
    
    """

    assets_path = Path(__file__).parent.parent / "dash_app" / "assets"

    dash_app= Dash(
        name="MatchAnalyzer",
        server=flask_app_server,
        suppress_callback_exceptions=True,
        assets_folder=assets_path,
        url_base_pathname="/dash/"
    )
    
    dash_app.title= "Select App"

    dash_app.layout= dash_main_container

    redirect_to_match_analyzer(dash_app)
    redirect_to_torque_analyzer(dash_app)
    main_log_out(dash_app)

    
    return dash_app

