import streamlit as st
import pandas as pd
import pydeck as pdk

# Load data function
@st.cache_data
def load_data():
    data = pd.read_csv("dataOUT/earthquakes.csv")
    # Clean data: Remove rows where LAT, LON, or MAG are NaN
    data = data.dropna(subset=["LAT", "LON", "MAG"])
    # Convert 'DATE' to datetime
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')
    return data

# Sidebar filters
def sidebar_filters(data):
    st.sidebar.header("Filter Earthquakes")

    # Magnitude filter
    min_mag, max_mag = st.sidebar.slider(
        "Select magnitude range",
        min_value=int(data['MAG'].min()),
        max_value=int(data['MAG'].max()),
        value=(int(data['MAG'].min()), int(data['MAG'].max())),
        step=1
    )

    # Date filter
    min_date, max_date = st.sidebar.date_input(
        "Select date range",
        [data['DATE'].min().date(), data['DATE'].max().date()]
    )
    
    # Filter data based on the user input
    filtered_data = data[
        (data['MAG'] >= min_mag) &
        (data['MAG'] <= max_mag) &
        (data['DATE'] >= pd.to_datetime(min_date)) &
        (data['DATE'] <= pd.to_datetime(max_date))
    ]
    
    return filtered_data

def run():
    # Load the earthquake data
    data = load_data()

    # Apply sidebar filters
    filtered_data = sidebar_filters(data)

    # If no data is available after filtering
    if filtered_data.empty:
        st.sidebar.warning("No data available for the selected filters.")
        return

    # Set up the 3D ColumnLayer
    layer = pdk.Layer(
        "ColumnLayer",
        data=filtered_data,
        get_position='[LON, LAT]',
        get_elevation="MAG * 50000",  # Elevation is the magnitude (scaled)
        elevation_scale=1,  # Scale factor for height (optional, adjust as needed)
        radius=5000,  # Radius of the column base
        get_fill_color="[255, 0, 0, 200]",  # Red color for the columns
        pickable=True,
        auto_highlight=True,
    )

    # Set up the view for the map
    view_state = pdk.ViewState(
        longitude=filtered_data["LON"].mean(),  # Center the view around the average longitude
        latitude=filtered_data["LAT"].mean(),   # Center the view around the average latitude
        zoom=2,  # Zoom level (adjust as needed)
        pitch=45,  # Tilt the map for a 3D effect
    )

    # Create the PyDeck Deck object with the 3D column layer
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Magnitude: {MAG}"},
    )

    # Show the PyDeck map in the Streamlit app
    st.pydeck_chart(deck)
