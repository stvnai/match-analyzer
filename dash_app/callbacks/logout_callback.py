from dash import Input, Output, dcc
from flask import url_for



def log_out(app):
    app.layout.children.append(dcc.Location(id="url-logout", refresh=True))

    @app.callback(
        Output("url-logout", "href"),
        Input("logout-button", "n_clicks"),
        prevent_initial_call=True
    )

    def handle_logout(n_clicks):
        if n_clicks:

            return url_for("main.logout")

def torque_log_out(app):
    app.layout.children.append(dcc.Location(id="torque-url-logout", refresh=True))

    @app.callback(
        Output("torque-url-logout", "href"),
        Input("torque-logout-button", "n_clicks"),
        prevent_initial_call=True
    )

    def handle_logout(n_clicks):
        if n_clicks:

            return url_for("main.logout")
        
def main_log_out(app):
    app.layout.children.append(dcc.Location(id="main-url-logout", refresh=True))

    @app.callback(
        Output("main-url-logout", "href"),
        Input("main-logout-button", "n_clicks"),
        prevent_initial_call=True
    )

    def handle_logout(n_clicks):
        if n_clicks:

            return url_for("main.logout")


