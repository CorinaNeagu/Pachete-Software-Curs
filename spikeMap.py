import streamlit as st
import pandas as pd
import pydeck as pdk
from sidebar import sidebar  

@st.cache_data
def load_data():
    data = pd.read_csv("dataOUT/earthquakes.csv")
    data = data.dropna(subset=["LAT", "LON", "MAG"])
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')
    return data

def run():
    data = load_data()

    filtered_data = sidebar(data)
    if filtered_data.empty:
        st.sidebar.warning("No data available for the selected filters.")
        return
    
    st.title("3D Spike Map")

    # Set up the 3D ColumnLayer with color gradient based on magnitude
    layer = pdk.Layer(
        "ColumnLayer",
        data=filtered_data,
        get_position='[LON, LAT]',
        get_elevation="MAG * 50000", 
        elevation_scale=1,  
        radius=5000,  
        get_fill_color="""
            [
                 MAG * 25.5,
                 255 - MAG * 25.5,         
                 MAG * 25.5,                     
                 200                 
            ]
            """,
        pickable=True,
        auto_highlight=True,
    )

    # Set up the view for the map with orientation and tilt
    view_state = pdk.ViewState(
        longitude=filtered_data["LON"].mean(),  
        latitude=filtered_data["LAT"].mean(),   
        zoom=3,  
        pitch=50,  
        bearing=30,  
    )

    # Create the PyDeck Deck map with the 3D columns
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Magnitude: {MAG}"},
    )

    st.pydeck_chart(deck)

