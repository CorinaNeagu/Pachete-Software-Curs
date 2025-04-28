import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, HeatMap

@st.cache_data
def load_data():
    data = pd.read_csv("dataIN/Carpathians_Earthquakes.csv", index_col=0)
    data.reset_index(inplace=True)

    data = data.drop(data.columns[list(range(3)) + list(range(-4, -1))], axis=1)
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')

    return data

def run():
    data = load_data()

    if "filters_applied" not in st.session_state:
        st.session_state.filters_applied = False

    if "filtered_data" not in st.session_state:
        st.session_state.filtered_data = data

    # Sidebar filtering options
    st.sidebar.title("Filter Earthquake Data")
    min_mag = st.sidebar.slider("Minimum Magnitude", 
                                min_value=float(data['MAG'].min()), 
                                max_value=float(data['MAG'].max()), 
                                value=4.0)
    years = data['DATE'].dt.year.unique()  
    start_year = st.sidebar.selectbox("Start Year", options=sorted(years), index=0)
    end_year = st.sidebar.selectbox("End Year", options=sorted(years), index=len(years)-1)

    # Filter button logic
    def apply_filters():
        filtered_data = data[
            (data['MAG'] >= min_mag) &
            (data['DATE'].dt.year >= start_year) &  
            (data['DATE'].dt.year <= end_year)
        ]
        st.session_state.filtered_data = filtered_data
        st.session_state.filters_applied = True

    def clear_filters():
        st.session_state.filtered_data = data
        st.session_state.filters_applied = False

    # Sidebar buttons
    apply_button = st.sidebar.button("Apply Filters", on_click=apply_filters)
    clear_button = st.sidebar.button("Clear Filters", on_click=clear_filters)

    #Map initialization
    earthquake_map = folium.Map(location=[20, 0], zoom_start=3)

    # Marker Clusters on the map
    marker_cluster = MarkerCluster().add_to(earthquake_map)

    # Markers on the map
    for _, row in st.session_state.filtered_data.iterrows():
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=folium.Popup(f"""
                <html>
                    <body>
                        <h4 style="font-size: 16px; font-weight: bold; color: #2d3e50;">Earthquake Information</h4>
                        <hr style="border: 1px solid #2d3e50;">
                        <p style="font-size: 14px; margin: 5px 0;"><strong>Location:</strong> {row['LAT']}, {row['LON']}</p>
                        <p style="font-size: 14px; margin: 5px 0;"><strong>Magnitude:</strong> {row['MAG']}</p>
                        <p style="font-size: 14px; margin: 5px 0;"><strong>Date:</strong> {row['DATE']}</p>
                        <p style="font-size: 14px; margin: 5px 0;"><strong>Time:</strong> {row['TIME']}</p>
                    </body>
                </html>
            """, max_width=300)
        ).add_to(marker_cluster)

    # Heatmap
    heat_data = [
        [row['LAT'], row['LON'], row['MAG']] 
        for _, row in st.session_state.filtered_data.dropna(subset=['LAT', 'LON', 'MAG']).iterrows()
    ]
    HeatMap(heat_data).add_to(earthquake_map)

    # Display the map
    st.title("Earthquake Heat & Cluster Map")
    st_folium(earthquake_map, width=800, height=500)

    with st.expander("Map Details & Interpretation"):
        st.markdown("""
    **What's on the map?**
    - Each marker represents an individual earthquake within the selected filters.
    - The **popup** on each marker shows detailed info: location, magnitude, date, and time.
    - The **heatmap layer** represents the density and magnitude of earthquakes in a region.
  
    **Interpreting the map:**
    - **Brighter or redder areas** on the heatmap suggest clusters of higher magnitude earthquakes.
    - **Dense marker clusters** in a region (especially after filtering) might indicate tectonic hotspots or seismic zones.
    - Use the sidebar to change the year or magnitude range to analyze how activity shifts over time.

    **Density (Spatial Clustering):**
    - Groupings based on the physical proximity of data points
    - In earthquake data, clustering can reveal significant patterns, such as:
        - **Seismic Hotspots**: Clusters of high-magnitude earthquakes in specific regions, indicating active seismic zones or tectonic plate boundaries (e.g., Vrancea Seismic Zone)
        - **Earthquake Frequency**: If a region has a lot of clustering over time, it may indicate that certain areas are more prone to seismic activity
        - **Seismic Patterns**: By looking at how clusters evolve over time, you might notice whether seismic activity increases or decreases in a particular area.

    **Clustering with Marker Clusters:**
    - Individual points are grouped together based on proximity, making it easier to visualize concentrations of events
        - **Zooming in**: As you zoom in, the markers will break apart, showing you exactly how many events are clustered in a region.
        - **Zooming out**: Clusters may form together into one larger marker, representing many events in that area.
    """)


