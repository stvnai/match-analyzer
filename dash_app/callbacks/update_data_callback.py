
from dash import Input, Output, State, callback
from dash_app.matchanalyzer import match_marker, compute_avg_matches, match_chart, match_summary_chart, match_time

def update_data_app(app):
    
    # Un solo callback para todos los pares
    @app.callback(
        [
            Output("power-slider", "value"), Output("power-input", "value"),
            Output("match-length-slider", "value"), Output("match-length-input", "value"),
            Output("rest-slider", "value"), Output("rest-input", "value"),
            Output("tolerance-slider", "value"), Output("tolerance-input", "value")
        ],
        
        [
            Input("power-slider", "value"), Input("power-input", "value"),
            Input("match-length-slider", "value"), Input("match-length-input", "value"),
            Input("rest-slider", "value"), Input("rest-input", "value"),
            Input("tolerance-slider", "value"), Input("tolerance-input", "value")
        ],
        
        prevent_initial_call=True
    )
    def sync_all_pairs(*values):
        from dash import ctx
        
        # Mapeo de inputs a sus pares
        pairs = {
            "power-slider": ("power-slider", "power-input"),
            "power-input": ("power-slider", "power-input"),
            "match-length-slider": ("match-length-slider", "match-length-input"),
            "match-length-input": ("match-length-slider", "match-length-input"),
            "rest-slider": ("rest-slider", "rest-input"),
            "rest-input": ("rest-slider", "rest-input"),
            "tolerance-slider": ("tolerance-slider", "tolerance-input"),
            "tolerance-input": ("tolerance-slider", "tolerance-input")
        }
        
        triggered = ctx.triggered_id
        if triggered in pairs:
            # Encontrar el valor que cambió
            input_index = list(pairs.keys()).index(triggered)
            new_value = values[input_index]
            
            # Actualizar ambos valores del par
            result = list(values)
            pair_ids = pairs[triggered]
            slider_index = list(pairs.keys()).index(pair_ids[0])
            input_index = list(pairs.keys()).index(pair_ids[1])
            
            result[slider_index] = new_value
            result[input_index] = new_value
            
            return result
        
        return values
    
    @app.callback(
            Output("matches-chart", "figure",allow_duplicate=True),
            Output("summary-chart", "figure",allow_duplicate=True),
            Output("match-time-h1", "children",allow_duplicate=True),
            Output("match-count-h1", "children",allow_duplicate=True),
            Output("power-trend-h1", "children",allow_duplicate=True),
            Output("power-trend-h1", "style",allow_duplicate=True),
            Output("gain-loss-h2", "children",allow_duplicate=True),
            Output("gain-loss-h1", "style",allow_duplicate=True),
            Output("gain-loss-h1", "children",allow_duplicate=True),

        [
            Input("power-input", "value"),
            Input("match-length-input", "value"),
            Input("rest-input", "value"),
            Input("tolerance-input", "value")
        ],
    
            State("data-store", "data"),
            prevent_initial_call=True
    )

    def update_charts_data(power, match_length, rest, tolerance, data):
        df= match_marker(data, power, match_length, rest, tolerance)
        matches_summary= compute_avg_matches(df)
        matches_fig= match_chart(df)
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
            

        power_trend_style= {"color": color}

        gain_loss_style= {"color":color}



        return matches_fig, summary_fig, match_time_value, match_count, trend_value, power_trend_style, gain_loss, gain_loss_style,percentage_value