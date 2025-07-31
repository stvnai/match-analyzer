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
            Output("power-trend-h1", "children",allow_duplicate=True),
            Output("power-trend-h1", "style"),
            Output("gain-loss-h2", "children",allow_duplicate=True),
            Output("gain-loss-h1", "style",allow_duplicate=True),
            Output("gain-loss-h1", "children",allow_duplicate=True),
            Output("main-content-area", "style"),
            Output("summ-metrics-container", "style"),
        
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
            summary_fig, trend=match_summary_chart(matches_summary)
            match_time_value= match_time(df)
            match_count= len(matches_summary)

            arrow_up = "▲"
            arrow_down = "▼"
            if len(trend) > 1:
                delta_trend=trend[-1] - trend[0]
                
                if delta_trend < 0:
                    color="#EB2C44"
                    trend_value= f"{trend[-1] - trend[0]:.1f}W {arrow_down}"
                    percentage= (trend[0] / trend[-1] -1) * 100
                    percentage_value= f"{percentage:.1f}% {arrow_down}"
                    gain_loss= "Loss %" 


                elif delta_trend > 0:
                    color= "#3AB04C"
                    trend_value= f"{trend[-1] - trend[0]:.1f}W {arrow_up}" 
                    percentage= (trend[-1] / trend[0] -1) * 100
                    percentage_value= f"{percentage:.1f}% {arrow_up}"
                    gain_loss= "Gain %" 
                else:
                    color="#a4a8bb"

            else:
                color="#a4a8bb"
                trend_value="--"
                gain_loss="Gain/Loss %:"
                percentage_value="--"


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









