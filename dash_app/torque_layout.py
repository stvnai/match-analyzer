import numpy as np
import plotly.graph_objects as go
from dash import dcc, html, Input, Output


#####*** HEADER CONTAINER ***#####
 
title_container= html.Div(
    id= "torque-title-container",
    className= "title-container",
    children= [html.H1("Torque Analyzer", className= "h1-title")]
)

uploader_component= dcc.Upload(
    id= "torque-file-uploader",
    className= "dash-uploader-area",
    multiple= False,
    accept=".FIT, .fit",
    children= [
        html.P("Drag and drop or"),
        html.A("click to browse .FIT file", style= {"font-weight":"bold"})
    ],
    style_reject={
        'borderStyle': 'dashed',
        'borderColor': '#1b5f8d', 
        'backgroundColor': 'rgba(27, 95, 141, 0.05)',
        'color': '#a4a8bb',
        'opacity': '0.8'
    }
)

uploader_container= html.Div(
    id= "torque-uploader-container",
    className= "uploader-container",
    children= [ uploader_component]
)

loading_data_container= html.Div(
    className="loading-container",
    children= dcc.Loading(
        id="torque-loading-data",
        delay_hide=1000,
        type="default",
        children= [html.Div(
            id="torque-loading-container",
            style={"display":"flex"}
            )
        ]
    )
)


header_container= html.Div(
    id= "torque-header-container",
    className= "header-container",
    children= [
        title_container,
        uploader_container,
        loading_data_container]
    )


#####*** METRICS CONTAINER ***#####

match_time_container= html.Div(
    id= "torque-match-time-container",
    className= "match-time-container",
    children= [
        html.H2("Torque Time", id= "torque-match-time-h2", className= "summ-metrics-h2"),
        html.H1("00:00:00", id= "torque-match-time-h1", className= "summ-metrics-h1")
    ]
)

match_count_container= html.Div(
    id= "torque-match-count-container",
    className= "match-count-container",
    children= [
        html.H2("Torque Count", id= "torque-match-count-h2", className= "summ-metrics-h2"),
        html.H1("0", id= "torque-match-count-h1", className= "summ-metrics-h1")
    ]
)

power_trend_container= html.Div(
    id= "torque-power-trend-container",
    className= "power-trend-container",
    children= [
        html.H2("Torque Trend", id= "torque-power-trend-h2", className= "summ-metrics-h2"),
        html.H1("0", id= "torque-power-trend-h1", className= "summ-metrics-h1")
    ]
)


gain_loss_container= html.Div(
    id= "torque-gain-loss-container",
    className= "gain-loss-container",
    children= [
        html.H2("--", id= "torque-gain-loss-h2", className= "summ-metrics-h2"),
        html.H1("--", id= "torque-gain-loss-h1", className= "summ-metrics-h1")
    ]
)

summ_metrics_container= html.Div(
    id= "torque-summ-metrics-container",
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
    id="torque-power-slider",
    className="input-slider",
    value=0.65,
    min=0.5,
    max=2.5,
    vertical=True,
    verticalHeight= 200,
    updatemode="drag",
    marks={
        0.5:"0.5",
        1.5:"1.5",
        2.5:"2.5"
    },
    tooltip={
        "placement": "left",
        "always_visible": True,
    }
)

power_slider_container= html.Div(
    id= "torque-power-inner-slider-container",
    className= "inner-slider-container",
    children=[power_slider]
)

match_length_slider= dcc.Slider(
    id="torque-match-length-slider",
    className="input-slider",
    value=15,
    min=5,
    max=1200,
    step=5,
    vertical=True,
    verticalHeight= 200,
    updatemode="drag",
    marks={
        10: "00:10",
        600:"10:00",
        1200:"20:00"
    },
    tooltip={
        "placement": "left",
        "always_visible": True,
    }
)

match_slider_container= html.Div(
    id= "torque-match-inner-slider-container",
    className= "inner-slider-container",
    children=[match_length_slider]
)

rest_slider= dcc.Slider(
    id="torque-rest-slider",
    className="input-slider",
    value=15,
    min=5,
    max=600,
    step=5,
    vertical=True,
    verticalHeight= 200,
    updatemode="drag",
    marks={
        10: "00:10",
        300:"05:00",
        600:"10:00"
    },
    tooltip={
        "placement": "left",
        "always_visible": True,
    }
)

rest_slider_container= html.Div(
    id= "torque-rest-inner-slider-container",
    className= "inner-slider-container",
    children=[rest_slider]
)

tolerance_slider= dcc.Slider(
    id="torque-tolerance-slider",
    className="input-slider",
    value=95,
    min=50,
    max=100,
    step=1,
    vertical=True,
    verticalHeight= 200,
    updatemode="drag",
    marks={
        50: "50%",
        75:"75%",
        100:"100%"
    },
    tooltip={
        "placement": "left",
        "always_visible": True,
    }
)

tolerance_slider_container= html.Div(
    id= "torque-tolerance-inner-slider-container",
    className= "inner-slider-container",
    children=[tolerance_slider]
)

#####*** PARAMETER INPUTS ***#####



power_input= dcc.Input(
    id="torque-power-input",
    className="input-fields",
    type="number",
    value=0.65,
    min=0.5,
    max=2.5
)

power_input_container= html.Div(
    id= "torque-power-inner-input-container",
    className= "inner-input-container",
    children=[power_input]
)



match_length_input= dcc.Input(
    id="torque-match-length-input",
    className="input-fields",
    type="number",
    value=15,
    min=5,
    max=1200,
)

match_input_container= html.Div(
    id= "torque-match-inner-input-container",
    className= "inner-input-container",
    children=[match_length_input]
)

rest_input= dcc.Input(
    id="torque-rest-input",
    className="input-fields",
    type="number",
    value=10,
    min=5,
    max=600,
)

rest_input_container= html.Div(
    id= "torque-rest-inner-input-container",
    className= "inner-input-container",
    children=[rest_input]
)

tolerance_input= dcc.Input(
    id="torque-tolerance-input",
    className="input-fields",
    type="number",
    value=95,
    min=50,
    max=100,
)

tolerance_input_container= html.Div(
    id= "torque-tolerance-inner-input-container",
    className= "inner-input-container",
    children=[tolerance_input]
)


#####*** PARAMETER NAMES ***#####


h3_power= html.H3("Torque", id="torque-h3-power", className="h3-inputs")

power_h3_container= html.Div(
    id= "torque-power-h3-inner-container",
    className="h3-inner-container",
    children= [h3_power]
)
h3_match_length= html.H3("Match Length", id="torque-h3-matchlength", className="h3-inputs")

match_h3_container= html.Div(
    id= "torque-match-h3-inner-container",
    className="h3-inner-container",
    children= [h3_match_length]
)

h3_rest= html.H3("Max Rest", id="torque-h3-rest", className="h3-inputs")

rest_h3_container= html.Div(
    id= "torque-rest-h3-inner-container",
    className="h3-inner-container",
    children= [h3_rest]
)

h3_tolerance= html.H3("Compliance", id="torque-h3-tolerance", className="h3-inputs")

tolerance_h3_container= html.Div(
    id= "torque-tolerance-h3-inner-container",
    className="h3-inner-container",
    children= [h3_tolerance]
)


#####*** PARAMETER UNITS ***#####


h3_power_units= html.H3("Nm/kg", id="torque-h3-power-units", className="h3-inputs-units")

power_h3_unit_container= html.Div(
    id= "torque-power-h3-unit-inner-container",
    className="h3-unit-inner-container",
    children= [h3_power_units]
)

h3_match_units= html.H3("s", id="torque-h3-match-units", className="h3-inputs-units")

match_h3_unit_container= html.Div(
    id= "torque-match-h3-unit-inner-container",
    className="h3-unit-inner-container",
    children= [h3_match_units]
)

h3_rest_units= html.H3("s", id="torque-h3-rest-units", className="h3-inputs-units")

rest_h3_unit_container= html.Div(
    id= "torque-rest-h3-unit-inner-container",
    className="h3-unit-inner-container",
    children= [h3_rest_units]
)

h3_tolerance_units= html.H3("%", id="torque-h3-tolerance-units", className="h3-inputs-units")

tolerance_h3_unit_container= html.Div(
    id= "torque-tolerance-h3-unit-inner-container",
    className="h3-unit-inner-container",
    children= [h3_tolerance_units]
)


#####*** WIDGETS CONTAINERS ***#####

power_container= html.Div(
    id="torque-power-container",
    className="widgets-container",
    children=[
        power_h3_unit_container,
        power_slider_container,
        power_input_container,
        power_h3_container
    ]
)
match_length_container= html.Div(
    id="torque-match-length-container",
    className="widgets-container",
    children=[
        match_h3_unit_container,
        match_slider_container,
        match_input_container,
        match_h3_container
    ]
)
rest_container= html.Div(
    id="torque-rest-container",
    className="widgets-container",
    children=[
        rest_h3_unit_container,
        rest_slider_container,
        rest_input_container,
        rest_h3_container
    ]
)

tolerance_container= html.Div(
    id="torque-tolerance-container",
    className="widgets-container",
    children=[
        tolerance_h3_unit_container,
        tolerance_slider_container,
        tolerance_input_container,
        tolerance_h3_container
    ]
)

all_inputs_container= html.Div(
    id= "torque-all-inputs-container",
    className= "all-inputs-container",
    children= [
        power_container,
        match_length_container,
        rest_container,
        tolerance_container
    ]
)

#####*** PARAMETERS CONTAINER ***#####

parameters_title_container= html.Div(
    id= "torque-parameter-title-container",
    className= "parameter-title-container",
    children= [html.H1("Parameters", className= "h1-parameter-title")]
)

parameters_container= html.Div(
    id="torque-parameters-container",
    className="parameters-container",
    children=[
        parameters_title_container,
        all_inputs_container
    ]
)


#####*** CHARTS CONTAINER ***#####

match_chart_container= html.Div(
    id= "torque-match-chart-container",
    className= "match-chart-container",
    children=[dcc.Graph(id="torque-matches-chart", className="matches-chart")]
)

summary_chart_container= html.Div(
    id= "torque-summary-chart-container",
    className= "summary-chart-container",
    children=[dcc.Graph(id="torque-summary-chart", className="summary-chart")]
)

charts_container= html.Div(
    id="torque-charts-container",
    className="charts-container",
    children=[
        match_chart_container,
        summary_chart_container
    ]
)



#####*** MAIN CONTENT AREA ***#####

data_area_container= html.Div(
    id= "torque-data-area-container",
    className= "data-area-container",
    children= [
        charts_container
    ]
)

main_content_area= html.Div(
    id= "torque-main-content-area",
    className= "main-content-area",
    children= [
        data_area_container,
        parameters_container,
    ],
    style={
        "display":"none",
        "flex-direction":"row",
        "transition": "0.2s ease-in"
    }
)
    


logout_button= html.Button(
    "Log Out",
    id="torque-logout-button",
    className="logout-button",
    style={"textDecoration": "none"})  


data_store= dcc.Store(id="torque-data-store")

return_button = html.A(
    "← Return",
    href="/dash/",  # o la ruta que necesites
    id="torque-return-button",
    className="return-button",
    style={"textDecoration": "none"}
)


torque_main_container= html.Div(
    id="torque-main-container",
    className="main-container",
    children= [
        return_button,
        logout_button,
        data_store,
        header_container,
        summ_metrics_container,
        main_content_area,
    ]
)




