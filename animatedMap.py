import pandas as pd
import plotly.express as px
import streamlit as st

def run():
    # Load data
    data = pd.read_csv("dataOUT/earthquakes.csv")
    
    # Clean up column names and date
    data.columns = data.columns.str.strip()
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')
    
    # Remove rows where DATE or MAG are missing
    data = data.dropna(subset=['DATE', 'MAG'])

    # Remove rows where MAG is negative or zero (invalid magnitudes)
    data = data[data['MAG'] > 0]
    
    # Create Plotly animated map
    fig = px.scatter_mapbox(data, 
                         lat='LAT', 
                         lon='LON', 
                         color='MAG',  # Color by magnitude
                         size='MAG',   # Size by magnitude
                         hover_name='DATE',  # Show date on hover
                         animation_frame=data['DATE'].dt.year.astype(str),
                         zoom=1,
                         height=600,
                         title="Earthquake Activity Over Time",
                         mapbox_style="carto-positron",  # Better-looking background
                        )

    # Show the animated map in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    if st.button("Back to Landing Page"):
        st.session_state.page = 'landing'
