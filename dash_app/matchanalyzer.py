import pandas as pd
import numpy as np
import plotly.graph_objects as go
from garmin_fit_sdk import Stream, Decoder
import os
import tempfile
import base64
import io


def extract_data(file):
    '''
    Extract metrics used for another feature engineer process.

    Args:
        filepath(str): string with absolute path to file being processed.
        name_id(str): string with the athlete's name introduced by the user in the GUI.

    Return:
        (tuple): data_df, metadata_df, csv_filename, filepath
    '''
    columns= [
    "date","elapsed_time","position_lat","position_long",
    "distance","elevation","speed","power","accumulated_power","heart_rate",
    "cadence","work","w_kg","kj_kg"
    ]

    try:
        content_type, content_string = file.split(',')
        decoded_bytes = base64.b64decode(content_string)
        data= io.BytesIO(decoded_bytes)

        stream= Stream.from_bytes_io(data)
        decoder= Decoder(stream)

        messages,_= decoder.read()

    except Exception as e:
        print(f"FATAL ERROR: Unable to read data from {file}: {e}")
        return

    try:
        
        filedate= messages["record_mesgs"][0]["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error with date in extract_data function: {e}. Date set to 1900-10-17")
        filedate= "1900-10-17"
    try:
        weight = messages.get('user_profile_mesgs',[{}])[0].get('weight',1)
    except Exception as e:

        print(f"Error in extract_data function {e}: Weight se to 1")
        weight=1

    try:
        data = messages.get("record_mesgs",[])
        if not data:
            print(f"WARNING: No data in {file}")
            data_df= pd.DataFrame()

        data_df=pd.DataFrame(data)

    except Exception as e:
        print(f"Error extracting records from file. DataFrame will be empty {file}: {e}")
        data_df=pd.DataFrame()
        data_df= data_df.convert_dtypes()



    if  data_df.empty:
        print(f"WARNING: No data in DataFrame. Returning empty DataFrame")
        data_df=pd.DataFrame(columns)

    else:

        data_df["elapsed_time"]= pd.to_datetime(range(len(data_df)), unit="s").strftime("%H:%M:%S")

        data_df["speed"] = np.round(data_df.get("enhanced_speed", np.nan) * 3.6,4)
        data_df["distance"] = np.round(data_df.get("distance", np.nan) / 1000,3)
        data_df["work"]= np.round(data_df.get("accumulated_power", np.nan)/1000,2)
        data_df["elevation"] = np.round(data_df.get("altitude", np.nan),2)


        if weight:
            data_df["w/kg"] = np.round(data_df.get("power",np.nan) / weight,2)
            data_df["kj/kg"]= np.round(data_df.get("accumulated_power", np.nan)/1000,2)


    for col in columns:
        if col not in data_df.columns:
            data_df[col]= np.nan
    data_df = data_df[columns].copy()

    df_processed= data_df.to_dict("records")


    return df_processed

# def load_and_process_file(uploaded_file):
#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix= ".fit") as temp_file:
#             temp_file.write(uploaded_file.getbuffer())
#             temp_filepath= temp_file.name

        
#         data, date= extract_data(temp_filepath)
    
#         return data, date
#     except Exception as e:
#             print("An error processing file has ocurred")
#     finally:
#             os.remove(temp_filepath)

def match_marker(data ,match_power= 200, match_length= 15, rest= 10, tolerance= 90) -> pd.DataFrame:
    
    df= pd.DataFrame.from_records(data)

    tolerance= tolerance/100
    min_required_values = int(tolerance*match_length)

    df["matches"] = 0

    df["match_count"] = 0
    in_match = False

    df["trigger"] = df["power"] >= match_power

    for i in range(len(df["trigger"])-match_length+1):

        if not df["trigger"].iloc[i]:
            continue

        window= df["power"].iloc[i:i+match_length]

        above_count = (window >= match_power).sum()

        below_count = 0
        max_below_consecutive = 0
        
        for val in window:
            if val < match_power:
                below_count +=1
                max_below_consecutive = max(max_below_consecutive, below_count)

            else:
                below_count = 0

        if above_count >= min_required_values and max_below_consecutive <= rest:

            df.loc[i:i+match_length-1, "matches"] = df["power"].iloc[i:i+match_length]

            if not in_match:
                df.loc[i,"match_count"] = 1
                in_match = True

        else:
            in_match = False
    
    df["power"] = df["power"].astype(float)
    df.drop(columns="trigger", inplace=True)

    return df.copy()

def compute_avg_matches(df: pd.DataFrame):
    """Calcula los promedios de los bloques de valores en la columna 'matches'."""
    avg_matches = []
    current_block = []

    for value in df["matches"]:
        if value != 0:
            current_block.append(value)
        elif current_block:
            avg_matches.append(sum(current_block) / len(current_block))
            current_block = []

    if current_block:  # Captura el último bloque si el DF termina sin ceros
        avg_matches.append(sum(current_block) / len(current_block))
    
    avg_matches= np.array(avg_matches).astype(int)
    return avg_matches


def process_matches(data, match_power, match_lenght, rest, tolerance):
    matches=match_marker(data, match_power, match_lenght, rest, tolerance)
    matches_summary= compute_avg_matches(matches)
    return matches, matches_summary

 # CHARTS

def match_chart(df):
    
    x=df["elapsed_time"]
    elevation=df["elevation"]
    power=df["power"]
    matches=df["matches"]
    work= df["work"]
    
    fig = go.Figure()

    #Elevation
    fig.add_trace(go.Scatter(
        x=x,
        y=elevation,
        name="Elevation",
        mode="lines",
        line= dict(color="rgba(128,128,128,0.8)", width=2),
        fill="tonexty",
        fillcolor="rgba(128,128,128,0.3)",
        yaxis="y2",
        
    ))

    #Power
    fig.add_trace(go.Scatter(
        x=x,
        y=power,
        mode="lines",
        name="Power",
        line= dict(color="rgba(27, 95, 141,1.0)", width=0.8)
        
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
        y=matches,
        mode="lines",
        name="Match",
        line= dict(color="red", width=0.9),
        fill="tozeroy",
        fillcolor="rgba(255, 0, 0,0.3)"
    ))


    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title="<b>Matches in Activity</b>",
        font=dict(color="rgb(161, 168, 180)"),
        xaxis=dict(
            fixedrange=False,
            showgrid=False,
            zeroline=True,
            tickfont=dict(color="rgb(161, 168, 180)",size=11)
        ),
        dragmode="zoom",
        height=320,
        width= 1300,
        xaxis_title="<b>Time</b>",
        margin=dict(l=125, r=125, t=40, b=10),




        yaxis= dict(
            title="<b>Power (W)</b>",
            title_font=dict(color="rgba(27, 95, 141,1.0)",size=13),
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



def match_summary_chart(array):

    
    x = np.arange(len(array))

    x_labels=[f"Match {i+1}" for i in range(len(array))]


    fig=go.Figure(data=go.Bar(
        x=x,
        y=array,
        marker_color="rgba(27, 95, 141,0.5)",
        name="Match", 
        hovertemplate='%{y} W')
        )
    if len(array) > 1:  # Evita error si solo hay un punto
        coef = np.polyfit(x, array, 1)  # Ajuste lineal (grado 1)
        trend_line = np.polyval(coef, x).astype(float)  # Evalúa la recta

        color= "rgb(161, 168, 180)"
        if trend_line[0] > trend_line[-1]:
            color= "rgb(235, 44, 68)"
        elif trend_line[0] < trend_line[-1]:
            color= "rgb(66, 199, 64)"

        else:
            color= "rgb(161, 168, 180)"

        # Agregar línea de tendencia
        
        fig.add_trace(go.Scatter(
            x=x,
            y=trend_line,
            mode="lines",
            name="Trend",
            line=dict(color=color, dash="longdash"),
            hovertemplate="%{y:.1f} W"
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
        height=190,
        width= 1300,
        title="<b>Matches Summary</b>",
        font=dict(color="rgb(161, 168, 180)"),
        xaxis_title="<b>Matches</b>",
        yaxis_title="Avg Power (W)",
        xaxis=dict(
            title_font=dict(color="rgb(161, 168, 180)",size=13),
            tickmode="array",
            tickvals=list(x),  
            ticktext=tick_list,
            tickangle=-30,
            tickfont=dict(color="rgb(161, 168, 180)",size=11)
        
        
    ),
    margin=dict(l=125, r=125, t=30, b=10),
    yaxis= dict(
            title="<b>Power (W)</b>",
            title_font=dict(color="rgba(27, 95, 141,1.0)",size=13),
            tickfont=dict(color="rgb(161, 168, 180)"),
            showgrid=False
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

    return fig


def match_time(df):
    match_time= (df['matches'] > 0).sum()
    match_time_formated=pd.to_timedelta(match_time,unit="s")
    total_time= str(match_time_formated).split(" ")[-1]

    return total_time