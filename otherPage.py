import streamlit as st
import pandas as pd

def run():
    # Back to landing page button
    if st.button("⬅ Back to Landing Page"):
        st.session_state.page = 'landing'
    
    # App title
    st.title("🌍 Earthquake Statistics Dashboard")
    st.markdown("Explore earthquake statistics and data visualizations.")

    # Load the data
    data = pd.read_csv("dataOUT/earthquakes.csv")
    
    # Clean column names (strip spaces)
    data.columns = data.columns.str.strip()

    # Convert DATE column to datetime format
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')

    # Drop rows where DATE is missing
    data = data.dropna(subset=['DATE'])

    # General Stats Section
    st.subheader("📊 General Statistics")
    st.write(f"**Total Earthquakes:** {len(data)}")
    st.write(f"**Date Range:** {data['DATE'].min().date()} to {data['DATE'].max().date()}")

    st.markdown("---")

    # Earthquakes per Year
    st.subheader("📅 Earthquakes Per Year")
    earthquakes_per_year = data.groupby(data['DATE'].dt.year).size().reset_index(name='Earthquake Count')
    
    # Sorting Option
    sort_option = st.selectbox(
        "Sort by Earthquake Count:",
        options=["Most Earthquakes", "Least Earthquakes"]
    )

    # Sort data based on user selection
    if sort_option == "Most Earthquakes":
        earthquakes_per_year = earthquakes_per_year.sort_values(by='Earthquake Count', ascending=False)
    else:
        earthquakes_per_year = earthquakes_per_year.sort_values(by='Earthquake Count', ascending=True)

    # Display sorted table
    st.dataframe(earthquakes_per_year)

    st.markdown("---")

    # Earthquakes Over Time Chart
    st.markdown('<h2 style="font-size:40px; color: #2d3e50;">🌍 Earthquakes Over Time</h2>', unsafe_allow_html=True)
    earthquakes_by_year = data.groupby(data['DATE'].dt.year).size()  # Count earthquakes per year
    st.line_chart(earthquakes_by_year)

    st.markdown("---")

    # Average Magnitude
    st.subheader("🔍 Earthquake Magnitude")
    st.write(f"**Average Magnitude:** {round(data['MAG'].mean(), 2)}")
    st.write(f"**Strongest Earthquake:** {data['MAG'].max()} magnitude")

    st.markdown("---")

    # Magnitude Distribution Chart
    st.subheader("📊 Magnitude Distribution")
    st.bar_chart(data['MAG'].value_counts().sort_index())

    st.markdown("---")

    # Depth vs Magnitude Scatter Chart
    st.subheader("🔬 Depth vs Magnitude")
    st.scatter_chart(data[['DEPTH', 'MAG']])

    st.markdown("---")


    if st.button("Back to Landing Page"):
        st.session_state.page = 'landing'
