import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sidebar import sidebar 

@st.cache_data
def load_data():
    data = pd.read_csv("dataOUT/earthquakes.csv")
    data.columns = data.columns.str.strip()

    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')
    
    data['DATETIME'] = pd.to_datetime(
        data['DATE'].dt.strftime('%Y-%m-%d') + ' ' + data['TIME'].astype(str),
        errors='coerce'
    )

    data = data.sort_values(by=['DATE', 'TIME']).reset_index(drop=True)
    data = data.dropna(subset=['LAT', 'LON', 'MAG', 'DATETIME'])
    return data

def run():
    data = load_data()

    filtered_data = sidebar(data)
    if 'DATETIME' not in filtered_data.columns:
        filtered_data['DATETIME'] = pd.to_datetime(
            filtered_data['DATE'].dt.strftime('%Y-%m-%d') + ' ' + filtered_data['TIME'].astype(str),
            errors='coerce'
        )
    if filtered_data.empty:
        st.sidebar.warning("No data available for the selected filters.")
        return

    # Title
    st.title("Earthquake Flow Map")
    st.markdown("Please zoom in to Central & Eastern Europe")

    # Sort data by full datetime
    filtered_data = filtered_data.sort_values(by='DATETIME').reset_index(drop=True)

    if len(filtered_data) < 2:
        st.warning("Not enough data to animate.")
        return

    # Initialize the plotly figure
    fig = go.Figure()
    frames = []

    # Creating frames for animation
    for i in range(1, len(filtered_data) + 1):
        data_subset = filtered_data.iloc[:i]
        lon_vals = data_subset['LON'].tolist()
        lat_vals = data_subset['LAT'].tolist()

        frames.append(go.Frame(
            data=[
                go.Scattermap(
                    mode='lines',
                    lon=lon_vals,
                    lat=lat_vals,
                    line=dict(width=2, color='blue'),
                    hoverinfo='text',
                    hovertext=[f"Datetime: {row['DATETIME']}<br>Magnitude: {row['MAG']}" for _, row in data_subset.iterrows()],
                )
            ],
            name=f"frame_{i}"
        ))

    # Adding empty initial trace fo r the map
    fig.add_trace(go.Scattermap(
        mode='lines',
        lon=[],
        lat=[],
        line=dict(width=2, color='blue'),
        hoverinfo='text',
        hovertext="",
    ))

    # Update layout and buttons for animation
    fig.update_layout(
        mapbox_style="carto-positron",  
        mapbox_zoom=4,  
        mapbox_center={"lat": filtered_data['LAT'].mean(), "lon": filtered_data['LON'].mean()},
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        title="Earthquake Flow Map (Chronological Path)",
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(
                label="Play",
                method="animate",
                args=[None, dict(frame=dict(duration=1000, redraw=True), fromcurrent=True)]
            )]
        )]
    )
    fig.frames = frames

    # Display the map animation
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Filtered Earthquake Data")

    earthquake_count = len(filtered_data)
    st.write(f"Number of Earthquakes: {earthquake_count}")

    st.dataframe(filtered_data[['DATETIME', 'LAT', 'LON', 'MAG']])