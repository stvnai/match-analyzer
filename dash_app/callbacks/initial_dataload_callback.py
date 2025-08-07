from garmin_fit_sdk import Stream, Decoder
from dash_app.matchanalyzer import extract_data,  match_marker, match_chart, summ_metric_values, match_time,compute_avg_matches,match_summary_chart
from dash_app.torqueanalyzer import extract_data,  torque_marker, torque_chart, torque_summ_metric_values, torque_time, compute_avg_torque, torque_summary_chart
from dash.exceptions import PreventUpdate

from dash import Input, Output, State
import time


def initial_load(app):

    @app.callback(

            Output("data-store", "data"),
            Output("matches-chart", "figure",allow_duplicate=True),
            Output("summary-chart", "figure",allow_duplicate=True),
            Output("match-time-h1", "children",allow_duplicate=True),
            Output("match-count-h1", "children",allow_duplicate=True),
            Output("power-trend-h1", "children",allow_duplicate=True),
            Output("power-trend-h1", "style"),
            Output("gain-loss-h2", "children",allow_duplicate=True),
            Output("gain-loss-h1", "style",allow_duplicate=True),
            Output("gain-loss-h1", "children",allow_duplicate=True),
            Output("main-content-area", "style"),
            Output("summ-metrics-container", "style"),


        
            Input("file-uploader", "contents"),
            Input("file-uploader", "filename"),

            State("power-input", "value"),
            State("match-length-input", "value"),
            State("rest-input", "value"),
            State("tolerance-input", "value"),

            prevent_initial_call=True
        
    )
    
    def process_file_and_initialize_charts(file_content, filename, power, match_length, rest, tolerance):

        filetype= filename.endswith(".fit") or filename.endswith(".FIT")
        if file_content and filetype:

            data= extract_data(file_content)

            df=match_marker(data, power, match_length, rest, tolerance)

            matches_summary= compute_avg_matches(df)
            initial_match_chart=match_chart(df)
            summary_fig, trend=match_summary_chart(matches_summary)
            match_time_value= match_time(df)
            match_count= len(matches_summary)
            color, trend_value, gain_loss, percentage_value= summ_metric_values(trend)


            data_container_style={
                "display":"flex",
                "transition": "0.2s ease-in"
            }
            summ_metrics_container= {
                "display":"flex",
                "transition":"0.2s ease-out"
            }

            power_trend_style= {"color": color}

            gain_loss_style= {"color":color}


            return data, initial_match_chart, summary_fig, match_time_value, match_count, trend_value, power_trend_style, gain_loss, gain_loss_style, percentage_value, data_container_style, summ_metrics_container
        
        else:
            raise PreventUpdate

    @app.callback(
        Output("loading-container", "style", allow_duplicate=True),
        Input("file-uploader", "contents"),
        Input("file-uploader", "filename"),
        prevent_initial_call=True
    )

    def show_loading_mesg(file_content:str, filename:str):
        filetype= filename.endswith(".fit") or filename.endswith(".FIT")
        if file_content and filetype:

            return {"display":"flex"}

        return {"display":"none"}
    

##### TORQUE CALLBACKS

def torque_initial_load(app):

    @app.callback(

            Output("torque-data-store", "data"),
            Output("torque-matches-chart", "figure",allow_duplicate=True),
            Output("torque-summary-chart", "figure",allow_duplicate=True),
            Output("torque-match-time-h1", "children",allow_duplicate=True),
            Output("torque-match-count-h1", "children",allow_duplicate=True),
            Output("torque-power-trend-h1", "children",allow_duplicate=True),
            Output("torque-power-trend-h1", "style"),
            Output("torque-gain-loss-h2", "children",allow_duplicate=True),
            Output("torque-gain-loss-h1", "style",allow_duplicate=True),
            Output("torque-gain-loss-h1", "children",allow_duplicate=True),
            Output("torque-main-content-area", "style"),
            Output("torque-summ-metrics-container", "style"),


        
            Input("torque-file-uploader", "contents"),
            Input("torque-file-uploader", "filename"),

            State("torque-power-input", "value"),
            State("torque-match-length-input", "value"),
            State("torque-rest-input", "value"),
            State("torque-tolerance-input", "value"),

            prevent_initial_call=True
        
    )
    
    def torque_process_file_and_initialize_charts(file_content, filename, newton_kg, match_length, rest, tolerance):

        filetype= filename.endswith(".fit") or filename.endswith(".FIT")
        if file_content and filetype:

            data= extract_data(file_content)

            df=torque_marker(data, newton_kg, match_length, rest, tolerance)

            matches_summary= compute_avg_torque(df)
            initial_match_chart=torque_chart(df)
            summary_fig, trend=torque_summary_chart(matches_summary)
            match_time_value= torque_time(df)
            match_count= len(matches_summary)
            color, trend_value, gain_loss, percentage_value= torque_summ_metric_values(trend)


            data_container_style={
                "display":"flex",
                "transition": "0.2s ease-in"
            }
            summ_metrics_container= {
                "display":"flex",
                "transition":"0.2s ease-out"
            }

            power_trend_style= {"color": color}

            gain_loss_style= {"color":color}

            
            return data, initial_match_chart, summary_fig, match_time_value, match_count, trend_value, power_trend_style, gain_loss, gain_loss_style, percentage_value, data_container_style, summ_metrics_container
        
        else:
            raise PreventUpdate

    @app.callback(
        Output("torque-loading-container", "style", allow_duplicate=True),
        Input("torque-file-uploader", "contents"),
        Input("torque-file-uploader", "filename"),
        prevent_initial_call=True
    )

    def torque_show_loading_mesg(file_content:str, filename:str):
        filetype= filename.endswith(".fit") or filename.endswith(".FIT")
        if file_content and filetype:

            return {"display":"flex"}

        return {"display":"none"}


