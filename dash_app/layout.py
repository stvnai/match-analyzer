import numpy as np
import plotly.graph_objects as go
from dash import dcc, html, Input, Output


#####*** HEADER CONTAINER ***#####
 
title_container= html.Div(
    id= "title-container",
    className= "title-container",
    children= [
        html.H1(
            "Match Analyzer",
            className= "h1-title"
        )
    ]
)

uploader_component= dcc.Upload(
            id= "file-uploader",
            className= "dash-uploader-area",
            multiple= False,
            accept=".FIT, .fit",
            children= [
                html.P("Drag and drop .FIT file here or"),
                html.A("click to browse.", style= {"font-weight":"bold"})
            ],
            style_reject={
        'borderStyle': 'dashed', # Mismo estilo de borde que el normal
        'borderColor': '#1b5f8d', # Mismo color de borde que el normal
        'backgroundColor': 'rgba(27, 95, 141, 0.05)', # Mismo fondo que el normal
        'color': '#a4a8bb', # Mismo color de texto que el normal
        'opacity': '0.8' # Asegura que no se vuelva transparente si Dash lo hace por defecto
    }
)

uploader_container= html.Div(
    id= "uploader-container",
    className= "uploader-container",
    children= [ uploader_component]
)

header_container= html.Div(
    id= "header-container",
    className= "header-container",
    children= [
        title_container,
        uploader_container
    ]
)

#####*** METRICS CONTAINER ***#####

match_time_container= html.Div(
    id= "match-time-container",
    className= "match-time-container",
    children= [
        html.H2(
            "Match Time:",
            id= "match-time-h2",
            className= "summ-metrics-h2"),
        html.H1(
            "00:00:00",
            id= "match-time-h1",
            className= "summ-metrics-h1")
    ]
)

match_count_container= html.Div(
    id= "match-count-container",
    className= "match-count-container",
    children= [
        html.H2(
            "Match Count:",
            id= "match-count-h2",
            className= "summ-metrics-h2"),
        html.H1(
            "0",
            id= "match-count-h1",
            className= "summ-metrics-h1")
    ]
)

power_trend_container= html.Div(
    id= "power-trend-container",
    className= "power-trend-container",
    children= [
        html.H2(
            "Power Trend:",
            id= "power-trend-h2",
            className= "summ-metrics-h2"),
        html.H1(
            "0",
            id= "power-trend-h1",
            className= "summ-metrics-h1")
    ]
)

gain_loss_container= html.Div(
    id= "gain-loss-container",
    className= "gain-loss-container",
    children= [
        html.H2(
            "None:",
            id= "gain-loss-h2",
            className= "summ-metrics-h2"),
        html.H1(
            "0%",
            id= "gain-loss-h1",
            className= "summ-metrics-h1")
    ]
)

summ_metrics_container= html.Div(
    id= "summ-metrics-container",
    className= "summ-metrics-container",
    children=[
        match_time_container,
        match_count_container,
        power_trend_container,
        gain_loss_container
    ],
        style={
            "display":"none",
            "transition": "0.2s ease-in"
    }
)

#####*** SLIDERS ***#####

power_slider= dcc.Slider(
    id="power-slider",
    className="input-slider",
    value=200,
    min=200,
    max=1200,
    marks={
        200:"200W",
        400:"400W",
        600:"600W",
        800:"800W",
        1000:"1000W",
        1200:"1200W"
    },
    vertical=True,
    verticalHeight= 200
)

match_length_slider= dcc.Slider(
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


rest_slider= dcc.Slider(
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

#####*** INPUTS ***#####

power_input= dcc.Input(
    id="power-input",
    className="input-fields",
    type="number",
    value=200,
    min=200,
    max=1200

)
match_length_input= dcc.Input(
    id="match-length-input",
    className="input-fields",
    type="number",
    value=10,
    min=10,
    max=600,

)

rest_input= dcc.Input(
    id="rest-input",
    className="input-fields",
    type="number",
    value=10,
    min=10,
    max=600,

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
h3_match_length= html.H3(
    "Match Length",
    id="h3-matchlength",
    className="h3-inputs"
)
h3_rest= html.H3(
    "Rest Time",
    id="h3-rest",
    className="h3-inputs"
)
h3_tolerance= html.H3(
    "% Compliance",
    id="h3-tolerance",
    className="h3-inputs"
)

#####*** PARAMETERS UNITS ***#####

h3_power_units= html.H3(
    "W",
    id="h3-power-units",
    className="h3-inputs-units"
)

h3_match_units= html.H3(
    "s",
    id="h3-match-units",
    className="h3-inputs-units"
)

h3_rest_units= html.H3(
    "s",
    id="h3-rest-units",
    className="h3-inputs-units"
)

h3_tolerance_units= html.H3(
    "%",
    id="h3-tolerance-units",
    className="h3-inputs-units"
)


#####*** WIDGETS CONTAINERS ***#####

power_container= html.Div(
    id="power-container",
    className="widgets-container",
    children=[
        h3_power_units,
        power_slider,
        power_input,
        h3_power
    ]
)
match_length_container= html.Div(
    id="match-length-container",
    className="widgets-container",
    children=[
        h3_match_units,
        match_length_slider,
        match_length_input,
        h3_match_length
    ]
)
rest_container= html.Div(
    id="rest-container",
    className="widgets-container",
    children=[
        h3_rest_units,
        rest_slider,
        rest_input,
        h3_rest
    ]
)

tolerance_container= html.Div(
    id="tolerance-container",
    className="widgets-container",
    children=[
        h3_tolerance_units,
        tolerance_slider,
        tolerance_input,
        h3_tolerance
    ]
)

#####*** PARAMETERS CONTAINER ***#####

parameters_title_container= html.Div(
    id= "parameter-title-container",
    className= "parameter-title-container",
    children= [
        html.H1(
            "Parameters",
            className= "h1-title"
        )
    ]
)

parameters_container= html.Div(
    id= "parameters-container",
    className= "parameters-container",
    children=[
        parameters_title_container,
        power_container,
        match_length_container,
        rest_container,
        tolerance_container
    ]

)


#####*** CHARTS CONTAINER ***#####

match_chart_container= html.Div(
    id= "match-chart-container",
    className= "match-chart-container",
    children=[
        dcc.Graph(id="matches-chart", className="matches-chart"),
    ]
)

summary_chart_container= html.Div(
    id= "summary-chart-container",
    className= "summary-chart-container",
    children=[
        dcc.Graph(id="summary-chart", className="summary-chart"),
    ]
)

charts_container= html.Div(
    id="charts-container",
    className="charts-container",
    children=[
        match_chart_container,
        summary_chart_container
    ]
)

#####*** MAIN CONTENT AREA ***#####

data_area_container= html.Div(
    id= "data-area-container",
    className= "data-area-container",
    children= [
        # summ_metrics_container,
        charts_container
    ]
)

main_content_area= html.Div(
    id= "main-content-area",
    className= "main-content-area",
    children= [
        data_area_container,
        parameters_container
    ],
    style={
            "display":"none",
            "flex-direction":"row",
            "transition": "0.2s ease-in"
    }
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
                            header_container,
                            summ_metrics_container,
                            main_content_area
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



