from garmin_fit_sdk import Stream, Decoder
from dash_app.matchanalyzer import extract_data,  match_marker, match_chart,match_time,compute_avg_matches,match_summary_chart
from dash.exceptions import PreventUpdate

from dash import Input, Output, State


def initial_load(app):

    @app.callback(

            Output("data-store", "data"),
            Output("matches-chart", "figure",allow_duplicate=True),
            Output("summary-chart", "figure",allow_duplicate=True),
            Output("match-time-h1", "children",allow_duplicate=True),
            Output("match-count-h1", "children",allow_duplicate=True),
            Output("sliders-container", "style"),
            Output("data-container", "style"),
        
            Input("file-uploader", "contents"),

            State("power-input", "value"),
            State("match-length-input", "value"),
            State("rest-input", "value"),
            State("tolerance-input", "value"),

            prevent_initial_call=True
        
    )
    
    def process_file_and_initialize_charts(file, power, match_length, rest, tolerance):

        if file:
       
            data= extract_data(file)

            df=match_marker(data, power, match_length, rest, tolerance)

            matches_summary= compute_avg_matches(df)
            initial_match_chart=match_chart(df)
            summary_fig=match_summary_chart(matches_summary)
            match_time_value= match_time(df)
            match_count= len(matches_summary)
        
            sliders_container_style= {
                "display":"flex",
                "transition":"0.2s ease-out"
            }

            data_container_style={
                "display":"flex",
                "flex-direction":"row",
                "transition": "0.2s ease-in"
            }

            return data, initial_match_chart, summary_fig, match_time_value,match_count, sliders_container_style,  data_container_style
        else:
            raise PreventUpdate
