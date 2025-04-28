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

def sidebar_filters(data):
    if "filters_applied" not in st.session_state:
        st.session_state.filters_applied = False

    if "filtered_data" not in st.session_state:
        st.session_state.filtered_data = data

    # Sidebar filtering options
    st.sidebar.title("Filter Earthquake Data")

    # Magnitude filter slider
    min_mag = st.sidebar.slider(
        "Minimum Magnitude",
        min_value=float(data['MAG'].min()),
        max_value=float(data['MAG'].max()),
        value=4.0
    )
    
    # Year filter
    years = data['DATE'].dt.year.unique()
    start_year = st.sidebar.selectbox("Start Year", options=sorted(years), index=0)
    end_year = st.sidebar.selectbox("End Year", options=sorted(years), index=len(years)-1)

    # Apply filters button
    def apply_filters():
        filtered_data = data[
            (data['MAG'] >= min_mag) &
            (data['DATE'].dt.year >= start_year) &  
            (data['DATE'].dt.year <= end_year)
        ]
        st.session_state.filtered_data = filtered_data
        st.session_state.filters_applied = True

    # Clear filters button
    def clear_filters():
        st.session_state.filtered_data = data
        st.session_state.filters_applied = False

    # Sidebar buttons for apply and clear filters
    apply_button = st.sidebar.button("Apply Filters", on_click=apply_filters)
    clear_button = st.sidebar.button("Clear Filters", on_click=clear_filters)

    return st.session_state.filtered_data

def run():
    # Load the earthquake data
    data = load_data()

    # Apply sidebar filters and session state
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


