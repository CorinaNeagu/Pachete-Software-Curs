import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    data = pd.read_csv("dataOUT/earthquakes.csv")
    
    # Clean column names
    data.columns = data.columns.str.strip()
    
    # Ensure 'DATE' is parsed as datetime
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')
    
    # Drop rows with missing LAT, LON, or MAG
    data = data.dropna(subset=['LAT', 'LON', 'MAG'])
    
    # Ensure all MAG values are non-negative for size
    data['size'] = data['MAG'].apply(lambda x: max(0, x))  # Apply correction to handle negative sizes
    
    return data

def run():
    data = load_data()

    # Create the bubble map using 'size' and 'MAG' for scaling
    fig = px.scatter_mapbox(data,
                         lat='LAT',
                         lon='LON',
                         size='size',  
                         color='MAG',
                         hover_name='TIME',
                         hover_data=['LAT', 'LON', 'MAG'],
                         title="Earthquake Magnitude vs Location",
                         template="plotly",
                         mapbox_style="carto-positron",
                         )

    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    if st.button("Back to Landing Page"):
        st.session_state.page = 'landing'
