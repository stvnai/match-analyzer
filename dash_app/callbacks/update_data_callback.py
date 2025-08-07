
from dash import Input, Output, State, callback
from dash_app.matchanalyzer import match_marker, compute_avg_matches, match_chart, match_summary_chart, match_time, summ_metric_values
from dash_app.torqueanalyzer import torque_marker, torque_chart, torque_summ_metric_values, torque_time, compute_avg_torque, torque_summary_chart

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
            Output("loading-container", "style", allow_duplicate=True),
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
        color, trend_value, gain_loss, percentage_value= summ_metric_values(trend)

        power_trend_style= {"color": color}

        gain_loss_style= {"color":color}
        updating_data_style = {"display":"none"}


        return matches_fig, summary_fig, match_time_value, match_count, trend_value, power_trend_style, gain_loss, gain_loss_style,percentage_value,updating_data_style
    
##### TORQUE CALLBACKS

def torque_update_data_app(app):
    
    # Un solo callback para todos los pares
    @app.callback(
        [
            Output("torque-power-slider", "value"), Output("torque-power-input", "value"),
            Output("torque-match-length-slider", "value"), Output("torque-match-length-input", "value"),
            Output("torque-rest-slider", "value"), Output("torque-rest-input", "value"),
            Output("torque-tolerance-slider", "value"), Output("torque-tolerance-input", "value")
        ],
        
        [
            Input("torque-power-slider", "value"), Input("torque-power-input", "value"),
            Input("torque-match-length-slider", "value"), Input("torque-match-length-input", "value"),
            Input("torque-rest-slider", "value"), Input("torque-rest-input", "value"),
            Input("torque-tolerance-slider", "value"), Input("torque-tolerance-input", "value")
        ],
        
        prevent_initial_call=True
    )
    def torque_sync_all_pairs(*values):
        from dash import ctx
        
        # Mapeo de inputs a sus pares
        pairs = {
            "torque-power-slider": ("torque-power-slider", "torque-power-input"),
            "torque-power-input": ("torque-power-slider", "torque-power-input"),
            "torque-match-length-slider": ("torque-match-length-slider", "torque-match-length-input"),
            "torque-match-length-input": ("torque-match-length-slider", "torque-match-length-input"),
            "torque-rest-slider": ("torque-rest-slider", "torque-rest-input"),
            "torque-rest-input": ("torque-rest-slider", "torque-rest-input"),
            "torque-tolerance-slider": ("torque-tolerance-slider", "torque-tolerance-input"),
            "torque-tolerance-input": ("torque-tolerance-slider", "torque-tolerance-input")
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
            Output("torque-matches-chart", "figure",allow_duplicate=True),
            Output("torque-summary-chart", "figure",allow_duplicate=True),
            Output("torque-match-time-h1", "children",allow_duplicate=True),
            Output("torque-match-count-h1", "children",allow_duplicate=True),
            Output("torque-power-trend-h1", "children",allow_duplicate=True),
            Output("torque-power-trend-h1", "style",allow_duplicate=True),
            Output("torque-gain-loss-h2", "children",allow_duplicate=True),
            Output("torque-gain-loss-h1", "style",allow_duplicate=True),
            Output("torque-gain-loss-h1", "children",allow_duplicate=True),
            Output("torque-loading-container", "style", allow_duplicate=True),
        [
            Input("torque-power-input", "value"),
            Input("torque-match-length-input", "value"),
            Input("torque-rest-input", "value"),
            Input("torque-tolerance-input", "value")
        ],
    
            State("torque-data-store", "data"),
            prevent_initial_call=True
    )

    def torque_update_charts_data(newton_kg, match_length, rest, tolerance, data):

        df= torque_marker(data, newton_kg, match_length, rest, tolerance)
        matches_summary= compute_avg_torque(df)
        matches_fig= torque_chart(df)
        summary_fig, trend=torque_summary_chart(matches_summary)
        match_time_value= torque_time(df)
        match_count= len(matches_summary)
        color, trend_value, gain_loss, percentage_value= torque_summ_metric_values(trend)

        power_trend_style= {"color": color}

        gain_loss_style= {"color":color}
        updating_data_style = {"display":"none"}


        
        return matches_fig, summary_fig, match_time_value, match_count, trend_value, power_trend_style, gain_loss, gain_loss_style,percentage_value,updating_data_style