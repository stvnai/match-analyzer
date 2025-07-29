import numpy as np
import plotly.graph_objects as go
from dash import dcc, html, Input, Output

# from callbacks.input_callbacks import *

h1_main_title= html.H1(
            "Match Analyzer",
            className="h1-title"
)

h2_main_subtitle= html.H2(
            "Upload .FIT file to extract matches",
            className="h2-title"
)

uploader_interface= dcc.Upload(
            id="file-uploader",
            multiple=False,
            children=html.Div("Drag and drop file here or click to browse file",className="dash-uploader"),
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "height": "4rem",
                "width": "50rem",
                "padding": "0px",
                "border": "2px solid #237bb6",
                "border-radius": "15px",
                "background-color": "transparent",
                "cursor":"pointer",
                "transition": "0.2s ease-out",
                "scale": "1.0"
            },
            style_active={
                'background-color': 'transparent',
                'border': "2px dashed #237bb6",
                "border-radius":"25px",
                "scale": "1.01",
                "transition": "0.2s ease-in"
            }
)


power_slider= dcc.Slider(
    id="power-slider",
    className="input-slider",
    value=200,
    min=200,
    max=1200,
    marks={200:"200W",400:"400W", 600:"600W",800:"800W",1000:"1000W", 1200:"1200W"},
    vertical=True,
    verticalHeight= 200
)
power_input= dcc.Input(
    id="power-input",
    className="input-fields",
    type="number",
    value=200,
    min=200,
    max=1200

)

match_lenght_slider= dcc.Slider(
    id="match-length-slider",
    className="input-slider",
    value=10,
    min=10,
    max=600,
    step=5,
    marks={
        10: "00:10",
        60:"01:00",
        180:"03:00",
        300:"05:00",
        480:"08:00",
        600:"10:00"
    },
    vertical=True,
    verticalHeight= 200
)

match_lenght_input= dcc.Input(
    id="match-length-input",
    className="input-fields",
    type="number",
    value=10,
    min=10,
    max=600,

)

rest_time_slider= dcc.Slider(
    id="rest-slider",
    className="input-slider",
    value=10,
    min=10,
    max=600,
    step=5,
        marks={
        10: "00:10",
        60:"01:00",
        180:"03:00",
        300:"05:00",
        480:"08:00",
        600:"10:00"
    },
    vertical=True,
    verticalHeight= 200

)

rest_input= dcc.Input(
    id="rest-input",
    className="input-fields",
    type="number",
    value=10,
    min=10,
    max=600,

)

tolerance_slider= dcc.Slider(
    id="tolerance-slider",
    className="input-slider",
    value=90,
    min=50,
    max=100,
    step=1,
        marks={
        50: "50%",
        75:"75%",
        100:"100%"
    },
    vertical=True,
    verticalHeight= 200

)

tolerance_input= dcc.Input(
    id="tolerance-input",
    className="input-fields",
    type="number",
    value=90,
    min=50,
    max=100,

)


h3_power= html.H3(
    "Power",
    id="h3-power",
    className="h3-inputs"
)
h3_power_units= html.H3(
    "W",
    id="h3-power-units",
    className="h3-inputs-units"
)

h3_match_lenght= html.H3(
    "Match Length",
    id="h3-matchlenght",
    className="h3-inputs"
)

h3_match_units= html.H3(
    "s",
    id="h3-match-units",
    className="h3-inputs-units"
)
h3_rest= html.H3(
    "Rest Time",
    id="h3-rest",
    className="h3-inputs"
)

h3_rest_units= html.H3(
    "s",
    id="h3-rest-units",
    className="h3-inputs-units"
)

h3_tolerance= html.H3(
    "% Compliance",
    id="h3-tolerance",
    className="h3-inputs"
)

h3_tolerance_units= html.H3(
    "%",
    id="h3-tolerance-units",
    className="h3-inputs-units"
)




title_container= html.Div(
    id="title_container",
    className="title_container",
    children= [
        h1_main_title,

        uploader_interface
    ]
)


power_container= html.Div(
    id="power_container",
    className="widgets_container",
    children=[
        h3_power,
        power_slider,
        power_input,
        h3_power_units
    ]
)
match_lenght_container= html.Div(
    id="match_length_container",
    className="widgets_container",
    children=[
        h3_match_lenght,
        match_lenght_slider,
        match_lenght_input,
        h3_match_units
    ]
)
rest_container= html.Div(
    id="rest_container",
    className="widgets_container",
    children=[
        h3_rest,
        rest_time_slider,
        rest_input,
        h3_rest_units
    ]
)
tolerance_container= html.Div(
    id="tolerance_container",
    className="widgets_container",
    children=[
        h3_tolerance,
        tolerance_slider,
        tolerance_input,
        h3_tolerance_units
    ]
)


sliders_container= html.Div(
    id="sliders-container",
    className="sliders-container",
    children= [
        power_container,
        match_lenght_container,
        rest_container,
        tolerance_container
    ],
    style= {
        "display":"none",
        "transition": "0.2s ease-out"}
)

charts_container= html.Div(
    id="charts-container",
    className="charts-container",
    children=[
        dcc.Graph(id="matches-chart",
                  className="matches-chart"),
        dcc.Graph(id="summary-chart",
                  className="matches-chart"),
    ]
)

match_time_display_container= html.Div(
    id="summary-display-container",
    className="match-time-container",
    children=[

        html.H2("Match Time:",id="match-time-h2",className="match-time-h2"),
        html.H1("00:00:00",id="match-time-h1",className="match-time-h1"),
        html.H2("Match Count:",id="match-count-h2",className="match-count-h2"),
        html.H1("0",id="match-count-h1",className="match-count-h1")
    ])



data_container= html.Div(
    id="data-container",
    className="data-container",
    children=[charts_container,
              match_time_display_container,
              ],
    style={"display":"none",
           "transition": "0.2s ease-out"}
              
)

logout_button= html.Button(
    "Log Out",
    id="logout-button",
    className="logout-button",
    style={"textDecoration": "none"})  


main_container= html.Div(id="main-container",
                         className="main-container",
                         children= [
                            logout_button,
                            dcc.Store(id="data-store"),
                            title_container,
                            sliders_container,
                            data_container
                            
                         ]
)




# app.layout = html.Div(
#     className="title_container",
#     id="title_container",
#     children=[
#         html.H1(
#             "Match Analyzer",className="h1-title"),
#         html.H2(
#             "Upload .FIT file to extract matches",className="h2-title"),
#         dcc.Upload(
#             id="file-uploader",
#             multiple=False,
#             children=html.Div("Select or Drag and Drop File",className="dash-uploader"),
#                 style={
#                     "display": "flex",
#                     "align-items": "center",
#                     "justify-content": "center",
#                     "height": "80px",
#                     "width": "500px",
#                     "padding": "0px",
#                     "border": "2px solid #1b5f8d",
#                     "border-radius": "25px",
#                     "background-color": "transparent",
#                     "cursor":"pointer",
#                     "transition": "0.2s ease-out",
#                     "scale": "1.0"
#                     },

                    

#                 style_active={
#                     'background-color': 'transparent',
#                     'border': "2px dashed #1b5f8d",
#                     "border-radius":"25px",
#                     "scale": "1.04",
#                     "transition": "0.2s ease-in"
#                     }
#                 )
#     ])

# app.layout= html.Div(
#     id="slider-container",
#     className="slider-container",
#     children= [
#         dcc.Slider(
#             id="power-slider",
#             value=120,
#             min=120,
#             max=1200,
#             marks={i: str(i) for i in range(120, 1201, 360)}
#         )
#     ])

# @app.callback(
#     Output("live-matches-graph", "figure"),
#     Input("slider-power", "value")
# )
# def update_graph(slider_value):
#     x= np.linspace(0,100, 100)
#     y= np.full_like(x,slider_value)

#     figure= go.Figure (data=[go.Scatter(
#             x=x,
#             y=y,
#             mode="lines",
#             line= dict(color="crimson", width=2),
#             name="Power point"
#         )])
    
#     figure.update_layout(title= f"Power= {slider_value}")
#     return figure



