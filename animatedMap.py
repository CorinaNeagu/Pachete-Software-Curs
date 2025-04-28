import pandas as pd
import plotly.express as px
import streamlit as st

def run():
    # Load data
    data = pd.read_csv("dataOUT/earthquakes.csv")
    
    # Clean up column names and date
    data.columns = data.columns.str.strip()
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')
    
    # Removing invalid rows
    data = data.dropna(subset=['DATE', 'MAG'])
    data = data[data['MAG'] > 0]
    
    fig = px.scatter_mapbox(data, 
                         lat='LAT', 
                         lon='LON', 
                         color='MAG',  
                         size='MAG',   
                         hover_name='DATE',  
                         animation_frame=data['DATE'].dt.year.astype(str),
                         zoom=3,
                         height=600,
                         title="Earthquake Activity Over Time",
                         mapbox_style="carto-positron",  
                        )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Map Details & Interpretation"):
        st.markdown("""
            Animated maps often use time as the variable to show how phenomena change over time. For example, an earthquake map might animate over years or months, 
            showing where and when earthquakes occurred, and their magnitudes or frequencies. This animation helps emphasize patterns, hotspots, or trends that are not as easily seen on a single snapshot.
            In this case, the earthquake animation shows the evolution of earthquake events, illustrating clusters, trends, and patterns over the years.
                    """)

 
