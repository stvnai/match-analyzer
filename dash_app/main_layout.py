import numpy as np
import plotly.graph_objects as go
from dash import dcc, html, Input, Output


#####*** HEADER CONTAINER ***#####
 
title_container= html.Div(
    id= "main-title-container",
    className= "title-container",
    children= [html.H1("Select Analyzer", className= "h1-main-title")]
)



header_container= html.Div(
    id= "main-header-container",
    className= "main-header-container",
    children= [
        title_container,
]
    )


#####*** METRICS CONTAINER ***#####

match_analyzer_button= html.Div(
    id= "match-analyzer-container",
    className= "app-analyzer-container",
    children= [
                # html.H1("Match Analyzer", id= "match-analyzer-h1", className= "match-analyzer-h1"),
                html.Button("Match Analyzer",id="match-analyzer-button", className="select-analyzer-button"),
                html.P("Analyze power output")
            ]
    )
torque_analyzer_button= html.Div(
    id= "torque-analyzer-container",
    className= "app-analyzer-container",
    children= [
                # html.H1("Torque Analyzer", id= "torque-analyzer-h1", className= "torque-analyzer-h1"),
                html.Button("Torque Analyzer", id="torque-analyzer-button",className="select-analyzer-button"),
                html.P("Analyze torque applied")
            ]
    )

select_app_container= html.Div(
    id= "select-app-container",
    className= "select-app-container",
    children=[
        match_analyzer_button,
        torque_analyzer_button
    ]
)


main_content_area= html.Div(
    id= "dash-main-content-area",
    className= "dash-main-content-area",
    children= [
        select_app_container
    ]
)
    


logout_button= html.Button(
    "Log Out",
    id="main-logout-button",
    className="logout-button",
    style={"textDecoration": "none"})  




match_analyzer_redirect= dcc.Location(id="redirect-to-match-analyzer", refresh=True)
torque_analyzer_redirect=dcc.Location(id="redirect-to-torque-analyzer", refresh=True)

dash_main_container= html.Div(
    id="dash-main-container",
    className="dash-main-container",
    children= [
        logout_button,
        header_container,
        main_content_area,
        match_analyzer_redirect,
        torque_analyzer_redirect
    ]
)




