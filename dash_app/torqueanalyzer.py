import pandas as pd
import numpy as np
import plotly.graph_objects as go
from garmin_fit_sdk import Stream, Decoder
import os
import base64
import io
from datetime import datetime


def torque_extract_data(file, weight=60):
    '''
    Extract metrics used for another feature engineer process.

    Args:
        filepath(str): string with absolute path to file being processed.
        name_id(str): string with the athlete's name introduced by the user in the GUI.

    Return:
        (tuple): data_df, metadata_df, csv_filename, filepath
    '''
    data_schema= {
        
        'elapsed_time': 'string',
        'distance': 'Float64',
        'elevation': 'Float64',
        'speed': 'Float64',
        'power': 'Int64',
        'nm': 'Float64',
        'nm_kg': 'Float64',
        "cadence": 'Int64',
        'heart_rate': 'Int64',
        'accumulated_power': 'Int64',
        'work': 'Float64',
        'w_kg': 'Float64',
        'kj_kg': 'Float64',
    }

    filename= os.path.basename(file)
    


    data_cols= list(data_schema.keys())
    data_df= pd.DataFrame(columns=list(data_schema.keys())).astype(data_schema)


    raw_data_df=pd.DataFrame()

    try:
        _, content_string = file.split(',')
        decoded_bytes = base64.b64decode(content_string)
        data= io.BytesIO(decoded_bytes)

        stream= Stream.from_bytes_io(data)
        decoder= Decoder(stream)
        messages,_= decoder.read()
        messages_keys= list(messages.keys())
        
    except Exception as e:
        print(f"CRITICAL ERROR: Unable to read data from {filename}: {e}.")  

        return raw_data_df
    
    date=datetime.now()
    if "session_mesgs" in messages:
        date= messages.get("session_mesgs")[0]["timestamp"]
    
    if "user_profile_mesgs" in messages_keys:
        try:
            weight = messages.get('user_profile_mesgs',[{}])[0].get('weight',60)
        except Exception as e:
            print(f"Error in extract_data function {e}: Weight set to 60kg")
            weight=60

    if "record_mesgs" in messages_keys:

        try:
            raw_data= messages.get('record_mesgs')
            raw_data_df= pd.DataFrame(raw_data)
        except Exception as e:
            print(f"Error building raw data dataframe from {filename}. Data will be empty {e}.")
            return raw_data_df
        
    ##### CHECK FOR ACCUMULATED POWER AVAILABLE #####

    if "accumulated_power" not in raw_data_df.columns:
        try:
            raw_data_df["accumulated_power"] = (raw_data_df["power"].cumsum() / 1000).round().astype("Int64")
        except Exception as e:
            raw_data_df["accumulated_power"] = pd.Series(0, dtype="Int64", index=raw_data_df.index)
            print(f"No power data to create accumulated power column from {filename}")


##### POPULATE DATA DATAFRAME WITH INITIAL RAW DATA #####

    raw_data_cols= raw_data_df.columns.to_list()
    for r_col in raw_data_cols:
        if r_col in data_cols:
            data_df[r_col]= raw_data_df[r_col]

# ELAPSED TIME

    data_df["elapsed_time"]= pd.to_datetime(range(len(raw_data_df)), unit="s").strftime("%H:%M:%S").astype("string")

## DISTANCE

    if "distance" in raw_data_cols:

        try:
            data_df["distance"]= (raw_data_df["distance"] / 1000).round(3).astype("Float64")
        except (ValueError, TypeError) as e:
            print(f"Error converting distance data from {filename}: {e}.")

    else:
        print(f"No data found for distance in {filename}.") 


## ELEVATION

    if "altitude" in raw_data_cols:
        
        try:
            data_df["elevation"]= (raw_data_df["altitude"]).round(1).astype("Float64")
        except (ValueError, TypeError) as e:
            print(f"Error converting elevation data from {filename}: {e}.")

    elif "enhanced_altitude" in raw_data_cols:

        try:
            data_df["elevation"]= (raw_data_df["enhanced_altitude"]).round(1).astype("Float64")
        except (ValueError, TypeError) as e:
            print(f"Error converting elevation data from {filename}: {e}.")

    else:
        print(f"No data found for elevation in {filename}.") 


## SPEED

    if "speed" in raw_data_cols:

        try:
            data_df["speed"]= (raw_data_df["speed"] * 3.6).round(2).astype("Float64")
        except (ValueError, TypeError) as e:
            print(f"Error with speed data from {filename}: {e}.")

    elif "enhanced_speed" in raw_data_cols:

        try:
            data_df["speed"]= (raw_data_df["enhanced_speed"] * 3.6).round(2).astype("Float64")
        except (ValueError, TypeError) as e:
            print(f"Error converting enhanced speed data from {filename}: {e}.") 

    else:
        print(f"No data found for speed in {filename}.")

##### ADITIONAL/DERIVATED METRICS #####

## WORK

    if "accumulated_power" in raw_data_cols:
        
        try:
            data_df["work"]= ((raw_data_df["accumulated_power"] / 1000)).round(2).astype("Float64")
        except (ValueError, TypeError) as e:
            print(f"Error converting work data from {filename}: {e}.")

    else:
        print(f"No data found for work in {filename}.")


# NM

    try:
        data_df["nm"]= ((raw_data_df["power"] * 60) / (2*(np.pi) * raw_data_df["cadence"])).round(2).astype("Float64")
    except (ValueError, TypeError) as e:
        print(f"Error with Nm data: {e}.")




## WEIGHT-RELATED METRICS


    try:    
        
        data_df["nm_kg"]= (data_df["nm"] / weight).round(2).astype("Float64")
    except (ValueError, TypeError) as e:
        print(f"Error converting Nm/kg data from {filename}: {e}.")

    try:    
        if "accumulated_power" in raw_data_cols:
            data_df["kj_kg"]= (raw_data_df["accumulated_power"] / 1000 / weight).round(2).astype("Float64")
    except (ValueError, TypeError) as e:
        print(f"Error converting kj_kg data from {filename}: {e}.")

    try:
        if "power" in raw_data_cols:
            data_df["w_kg"]= (raw_data_df["power"] / weight).round(2).astype("Float64")
    except (ValueError, TypeError) as e:
        print(f"Error converting w_kg data {filename}: {e}.")
        




    df_processed= data_df.to_dict("records")


    return df_processed, date



def torque_marker(data ,newton_kg= 0.65, match_length= 15, rest= 10, tolerance= 90) -> pd.DataFrame:
    
    df= pd.DataFrame.from_records(data)


    tolerance= tolerance/100
    min_required_values = int(tolerance*match_length)

    df["torque"] = pd.Series(0.0, dtype="Float64", index=df.index)

    df["match_count"] = 0
    in_match = False

    df["trigger"] = df["nm_kg"] >= newton_kg

    for i in range(len(df["trigger"])-match_length+1):

        if not df["trigger"].iloc[i]:
            continue

        window= df["nm_kg"].iloc[i:i+match_length]

        above_count = (window >= newton_kg).sum()

        below_count = 0
        max_below_consecutive = 0
        
        for val in window:
            if val < newton_kg:
                below_count +=1
                max_below_consecutive = max(max_below_consecutive, below_count)

            else:
                below_count = 0

        if above_count >= min_required_values and max_below_consecutive <= rest:

            df.loc[i:i+match_length-1, "torque"] = df["nm_kg"].iloc[i:i+match_length].astype("Float64")

            if not in_match:
                df.loc[i,"match_count"] = 1
                in_match = True

        else:
            in_match = False
    
    df.drop(columns="trigger", inplace=True)

    return df.copy()

def compute_avg_torque(df: pd.DataFrame):

    """Calcula los promedios de los bloques de valores en la columna 'torque'."""
    avg_matches = []
    current_block = []
    test_array= []

    for i, row in df.iterrows():
        if row["match_count"] == 1:

            current_block.append(row["torque"])
        elif row["match_count"] == 0:
            
            if current_block:
                avg_matches.append(sum(current_block) / len(current_block))
                current_block = []

    
    if current_block:
        avg_matches.append(sum(current_block) / len(current_block))
    
    avg_matches= np.array(avg_matches, dtype=np.float64)
    return avg_matches


def process_torque(data, newton_kg, match_lenght, rest, tolerance):
    matches=torque_marker(data, newton_kg, match_lenght, rest, tolerance)
    matches_summary= compute_avg_torque(matches)
    return matches, matches_summary

 # CHARTS

def torque_chart(df, date):
    
    x=df["elapsed_time"]
    elevation=df["elevation"]
    power=df["power"]
    newton_kg=df["nm_kg"]
    torque=df["torque"]
    work= df["work"]
    
    fig = go.Figure()

    #Elevation
    fig.add_trace(go.Scatter(
        x=x,
        y=elevation,
        name="Elevation",
        mode="lines",
        line= dict(color="rgba(128,128,128,0.8)", width=1.5),
        fill="tonexty",
        fillcolor="rgba(128,128,128,0.1)",
        yaxis="y2",
        
    ))

    #Power
    fig.add_trace(go.Scatter(
        x=x,
        y=power,
        mode="lines",
        name="Power",
        line= dict(color="#1a6395", width=0.8)
        
    ))

    fig.add_trace(go.Scatter(
        x=x,
        y=newton_kg,
        mode="lines",
        name="Nm/kg",
        line= dict(color="#ef900b", width=0.8),
        yaxis="y4"
        
    ))

    #Work
    fig.add_trace(go.Scatter(
        x=x,
        y=work,
        mode="lines",
        name="Work",
        line= dict(color="rgba(0, 165, 143,.8)", width=0.8),
        yaxis="y3"
        

    ))
    #Matches
    fig.add_trace(go.Scatter(
        x=x,
        y=torque,
        mode="lines",
        name="Torque",
        line= dict(color="rgba(235, 44, 68, 0.6)", width=0.8),
        fill="tozeroy",
        fillcolor="rgba(235, 44, 68,0.2)",
        yaxis="y4"
    ))


    fig.update_layout(
        
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=f"<b>Selected torque segments</b> {date}",
        font=dict(color="rgb(161, 168, 180)"),
        xaxis=dict(
            fixedrange=False,
            showgrid=False,
            zeroline=True,
            tickfont=dict(color="rgb(161, 168, 180)",size=11)
        ),
        dragmode="zoom",

        xaxis_title="<b>Time</b>",
        margin=dict(l=125, r=125, t=40, b=10),




        yaxis= dict(
            title="<b>Power (W)</b>",
            title_font=dict(color="#1a6395",size=13),
            title_standoff=40,
            side="left",
            range=[0,max(df["power"]) +200],
            showgrid=False,
            zeroline=True,
            domain=[0.1, 0.9],
            tickcolor="rgba(27, 95, 141,1.0)",
            
            position=0,
            tickfont=dict(color="rgba(27, 95, 141,1.0)"),
            fixedrange=True         
        ),
        
        yaxis2=dict(
            title="<b>Elevation (m)</b>",
            title_font=dict(color="rgba(145,145,145,1.0)",size=13),
            overlaying="y",
            title_standoff=36,
            side="right",
            type="log",
            tickmode="array",
            layer="below traces",
            anchor="free",
            showgrid=False,
            position=1,
            tickcolor="rgba(135,135,135,1.0)",
            tickfont=dict(color="rgba(135,135,135,1.0)"),
            fixedrange=True
            
            
            
        ),
        yaxis3=dict(
            title="<b>Work (kJ)</b>",
            title_font=dict(color="rgba(0, 165, 143,1.0)",size=12),
            title_standoff=36,
            overlaying="y",
            side="left",
            tickmode="array",
            tickvals=[10, 50, 100, 500, 1000, 2000, 5000, 8000],
            range=[0,max(work)+500],
            layer="below traces",
            showgrid=False,
            anchor="free",
            position=0.024,
            tickcolor="rgba(0, 165, 143,1.0)",
            tickfont=dict(color="rgba(0, 165, 143,1.0)", size=11),
            fixedrange=True  
            
            ),

        yaxis4=dict(
            title="<b>Torque (Nm/kg)</b>",
            title_font=dict(color="rgb(239, 144, 11)",size=12),
            title_standoff=50,
            overlaying="y",
            side="right",
            tickmode="array",
            tickvals=[0.0, 0.5, 0.6, 0.7, 0.8, 0.9 , 1.0, 1.5, 2.0, 2.5],
            rangemode="tozero",
            range=[0.0,max(newton_kg)+0.5],
            layer="below traces",
            showgrid=False,
            anchor="free",
            position=0.96,
            tickcolor="rgb(239, 144, 11)",
            tickfont=dict(color="rgb(239, 144, 11)", size=11),
            fixedrange=True  
            
            ),

        legend=dict(
        x=1.06,  # Izquierda
        y=0.8,  # Abajo
        xanchor="left",
        yanchor="bottom"

        ),
 
        hovermode="x unified",

        hoverlabel=dict(
        bgcolor="rgba(45, 45, 45, 0.85)",
        font_color="white",
        bordercolor="rgba(70, 70, 70, 0.6)"
        )
             
    )


    fig.update_xaxes(

        nticks=df.shape[0]//1000,
        tickformat="%H:%M:%S",
        tickmode="auto",
        tickangle=-30,
        showspikes=True,
        spikemode='across',
        spikesnap='cursor',
        spikecolor='rgba(200, 200, 200, 0.8)',
        spikethickness=-2,                     
        spikedash='dash')
    

    return fig


#MATCH SUMMARY CHART



def torque_summary_chart(array):

    
    x = np.arange(len(array))

    x_labels=[f"Torque {i+1}" for i in range(len(array))]


    fig=go.Figure(data=go.Bar(
        x=x,
        y=array,
        marker_color="rgba(0, 119, 143, 0.6)",
        name="Torque", 
        hovertemplate='%{y:.2f} Nm/kg')
        )
    if len(array) > 1:
        coef = np.polyfit(x, array, 1)
        trend_line = np.polyval(coef, x).astype(float)

        color= "rgb(161, 168, 180)"
        if trend_line[0] > trend_line[-1]:
            color= "#EB2C44"
        elif trend_line[0] < trend_line[-1]:
            color= "#3AB04C"

        else:
            color= "rgb(161, 168, 180)"

        # Agregar línea de tendencia
        
        fig.add_trace(go.Scatter(
            x=x,
            y=trend_line,
            mode="lines",
            name="Trend",
            line=dict(color=color, dash="dot"),
            hovertemplate="%{y:.2f} Nm/kg"
        ))
    else:
        trend_line =np.array([])

    

    tick_list= []
    if len(x_labels) > 10:
        for i, label in enumerate(x_labels):
            if i % 3 == 0:  # Muestra la etiqueta para el índice 0, 2, 4, etc.
                tick_list.append(label)
            else:
                tick_list.append('')
    else:
        tick_list= x_labels

    fig.update_layout(
        
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title="<b>Torque segments summary</b>",
        font=dict(color="rgb(161, 168, 180)"),
        xaxis_title="<b>Torque Segments</b>",
        yaxis_title="Torque (nm/kg)",
        margin=dict(l=125, r=125, t=30, b=10),
        
        xaxis=dict(
            title_font=dict(color="rgb(161, 168, 180)",size=13),
            tickmode="array",
            tickvals=list(x),  
            ticktext=tick_list,
            tickangle=-30,
            tickfont=dict(color="rgb(161, 168, 180)",size=11)
            
            
        ),
        yaxis= dict(
            title="<b>Torque (Nm/kg)</b>",
            title_font=dict(color="rgba(0, 119, 143, 1)",size=13),
            tickfont=dict(color="rgba(0, 119, 143, 1)"),
            showgrid=False,
            fixedrange=True  
        ),

        hovermode="x unified",

        hoverlabel=dict(
            bgcolor="rgba(45, 45, 45, 0.85)",
            font_color="rgb(161, 168, 180)",
            bordercolor="rgba(70, 70, 70, 0.6)"
        )
                
        )

    fig.update_xaxes(
        # tickmode="auto",
        showspikes=True,
        spikemode='across',
        spikesnap='cursor',
        spikecolor='rgba(200, 200, 200, 0.8)',
        spikethickness=-2,                     
        spikedash='dash')

    return fig, trend_line


def torque_time(df):
    match_time= (df["torque"] > 0).sum()
    match_time_formated=pd.to_timedelta(match_time,unit="s")
    total_time= str(match_time_formated).split(" ")[-1]

    return total_time


def torque_summ_metric_values(array):
    
    arrow_up = "▲"
    arrow_down = "▼"

    color="#a4a8bb"
    trend_value="--"
    gain_loss="Gain/Loss %:"
    percentage_value="--"

    if len(array) < 2:
        return color, trend_value, gain_loss, percentage_value


    try:
        delta_trend= array[-1] - array[0]

        if delta_trend < 0:

            color="#EB2C44"
            trend_value= f"{array[-1] - array[0]:.2f}Nm/kg {arrow_down}"

            percentage= (array[0] / array[-1] - 1) * 100
            percentage_value= f"{percentage:.1f}% {arrow_down}"
            gain_loss= "Loss %" 

        elif delta_trend > 0:

            color= "#3AB04C"
            trend_value= f"{array[-1] - array[0]:.2f}Nm/kg {arrow_up}"

            percentage= (array[-1] / array[0] - 1) * 100
            percentage_value= f"{percentage:.1f}% {arrow_up}"
            gain_loss= "Gain %" 

    except Exception as e:
        return color, trend_value, gain_loss, percentage_value

    return color, trend_value, gain_loss, percentage_value