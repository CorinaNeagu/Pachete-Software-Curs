import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    data = pd.read_csv("dataOUT/earthquakes.csv")
    data.columns = data.columns.str.strip()
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')
    data = data.dropna(subset=['LAT', 'LON', 'MAG'])

    data['size'] = data['MAG'].apply(lambda x: max(0, x)) # all MAG values are non-negative for size
    
    return data

def run():
    data = load_data()
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


