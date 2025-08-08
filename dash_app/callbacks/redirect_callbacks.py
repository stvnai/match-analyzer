from dash import Input, Output
from flask import url_for, redirect

def redirect_to_match_analyzer(app):
    @app.callback(
        Output("redirect-to-match-analyzer", "href"),
        Input("match-analyzer-button", "n_clicks")
    )
    def handle_redirect_match_analyzer(n_clicks):
        if n_clicks:
            return "/dash/match-analyzer/"
        

def redirect_to_torque_analyzer(app):
    @app.callback(
        Output("redirect-to-torque-analyzer", "href"),
        Input("torque-analyzer-button", "n_clicks")
    )
    def handle_redirect_match_analyzer(n_clicks):
        if n_clicks:
            return "/dash/torque-analyzer/"