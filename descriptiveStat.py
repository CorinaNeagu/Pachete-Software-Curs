import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def run():
    st.title("🌍 Earthquake Statistics Dashboard")
    data = pd.read_csv("dataOUT/earthquakes.csv")
    
    data.columns = data.columns.str.strip()
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')
    data = data.dropna(subset=['DATE'])
    data = data[(data['MAG'] > 0) & (data['DEPTH'] > 0)]


    basic_stats = {
        "Total Earthquakes": len(data),
        "Minimum Magnitude": data['MAG'].min(),
        "Maximum Magnitude": data['MAG'].max(),
        "Median Magnitude": data['MAG'].median(),
        "Mean Magnitude": data['MAG'].mean(),
        "Standard Deviation (Magnitude)": data['MAG'].std(),
        "Mode Magnitude": data['MAG'].mode()[0] if not data['MAG'].mode().empty else None,
        "Average Depth (km)": data['DEPTH'].mean(),
        "Shallowest Earthquake (km)": data['DEPTH'].min(),
        "Deepest Earthquake (km)": data['DEPTH'].max()
    }

    st.subheader("📌 Summary Statistics")
    for stat, value in basic_stats.items():
        st.write(f"**{stat}:** {round(value, 2) if isinstance(value, (int, float)) else value}")

    st.markdown("---")

    # Earthquakes per Year
    st.subheader("📅 Earthquakes Per Year")
    earthquakes_per_year = data.groupby(data['DATE'].dt.year).size().reset_index(name='Earthquake Count')
    
    # Sorting Option
    sort_option = st.selectbox(
        "Sort by Earthquake Count:",
        options=["Most Earthquakes", "Least Earthquakes"]
    )

    if sort_option == "Most Earthquakes":
        earthquakes_per_year = earthquakes_per_year.sort_values(by='Earthquake Count', ascending=False)
    else:
        earthquakes_per_year = earthquakes_per_year.sort_values(by='Earthquake Count', ascending=True)

    st.dataframe(earthquakes_per_year)

    st.markdown("---")

    st.subheader("⚡ Top 5 Largest Earthquakes")
    top_earthquakes = data[['DATE', 'LAT', 'LON', 'MAG']].sort_values(by='MAG', ascending=False).head(5)
    st.write(top_earthquakes)

    st.markdown("---")

    # Earthquakes Over Time Chart
    st.markdown('<h2 style="font-size:40px; color: #2d3e50;">🌍 Earthquakes Over Time</h2>', unsafe_allow_html=True)
    earthquakes_by_year = data.groupby(data['DATE'].dt.year).size()  
    st.line_chart(earthquakes_by_year)

    st.markdown("---")

    # Magnitude Distribution Chart
    st.subheader("📊 Magnitude Distribution")
    st.bar_chart(data['MAG'].value_counts().sort_index())

    st.markdown("---")

    # Earthquakes by Month
    data['Month'] = data['DATE'].dt.month
    monthly_counts = data['Month'].value_counts().sort_index()

    # Earthquakes by Day of Week
    available_years = data['DATE'].dt.year.dropna().unique()
    selected_year = st.selectbox("Select Year for Day of the Week Analysis", sorted(available_years))
   
    yearly_data = data[data['DATE'].dt.year == selected_year]
    yearly_data['Weekday'] = yearly_data['DATE'].dt.day_name()
    
    weekday_counts = yearly_data['Weekday'].value_counts()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_counts = weekday_counts.reindex(weekday_order).fillna(0)

    st.subheader(f"📅 Earthquakes by Day of the Week in {selected_year}")
    st.bar_chart(weekday_counts)


    # Cumulative Earthquake Count Over Time
    data['Year'] = data['DATE'].dt.year
    cumulative_data = data.groupby('Year').size().cumsum()

    # Average Magnitude per Year
    avg_mag_per_year = data.groupby('Year')['MAG'].mean()

    # Depth vs Magnitude Correlation
    correlation = data['DEPTH'].corr(data['MAG'])

    st.markdown("---")

    # Earthquakes by Month (with year selection)
    st.subheader("🗓️ Earthquakes by Month")
    
    available_years = data['DATE'].dt.year.dropna().unique()
    selected_year_month = st.selectbox("Select Year for Monthly Analysis", sorted(available_years))
    
    yearly_month_data = data[data['DATE'].dt.year == selected_year_month]
    yearly_month_data['Month'] = yearly_month_data['DATE'].dt.month
    monthly_counts = yearly_month_data['Month'].value_counts().sort_index()
    
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    monthly_counts.index = monthly_counts.index.map(month_names)
    st.bar_chart(monthly_counts)


    st.markdown("---")

    # Average Magnitude per Year
    st.subheader("📊 Average Magnitude per Year")
    st.line_chart(avg_mag_per_year)

    st.markdown("---")

    # Depth vs Magnitude Correlation
    st.subheader("🔗 Depth vs Magnitude Correlation")

    min_mag_val = float(data['MAG'].min())
    max_mag_val = float(data['MAG'].max())
    min_depth_val = float(data['DEPTH'].min())
    max_depth_val = float(data['DEPTH'].max())

    mag_range = st.slider(
        "Select Magnitude Range:",
        min_value=round(min_mag_val, 1),
        max_value=round(max_mag_val, 1),
        value=(round(min_mag_val, 1), round(max_mag_val, 1)),
        step=0.1
    )

    depth_range = st.slider(
        "Select Depth Range (km):",
        min_value=int(min_depth_val),
        max_value=int(max_depth_val),
        value=(int(min_depth_val), int(max_depth_val)),
        step=10
    )

    filtered_corr_data = data[
        (data['MAG'] >= mag_range[0]) & (data['MAG'] <= mag_range[1]) &
        (data['DEPTH'] >= depth_range[0]) & (data['DEPTH'] <= depth_range[1])
    ]

    if filtered_corr_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        correlation = filtered_corr_data['DEPTH'].corr(filtered_corr_data['MAG'])
        st.write(f"**Filtered Pearson Correlation Coefficient:** {round(correlation, 3)}")

    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)

    with col1:
        with st.expander("r = +1 (Perfect Positive Correlation)"):
            st.markdown("""
                **Interpretation:** A perfect positive linear relationship between the two variables. 
                As one variable increases, the other increases proportionally and in a perfectly straight line.
            """)

    with col2:
        with st.expander("r = -1 (Perfect Negative Correlation)"):
            st.markdown("""
                **Interpretation:** A perfect negative linear relationship between the two variables. 
                As one variable increases, the other decreases proportionally and in a perfectly straight line.
            """)

    with col3:
        with st.expander("0.7 ≤ r < 1 (Strong Positive Correlation)"):
            st.markdown("""
                **Interpretation:** A strong positive relationship. As one variable increases, the other tends to increase as well, and the relationship is nearly linear, but not perfectly.
            """)

    with col4:
        with st.expander("0.3 ≤ r < 0.7 (Moderate Positive Correlation)"):
            st.markdown("""
                **Interpretation:** A moderate positive relationship. As one variable increases, the other tends to increase, but with noticeable deviations.
            """)

    # Second row of expanders
    with col5:
        with st.expander("0 < r < 0.3 (Weak Positive Correlation)"):
            st.markdown("""
                **Interpretation:** A weak positive relationship. There is a slight tendency for one variable to increase as the other increases, but the relationship is weak.
            """)

    with col6:
        with st.expander("r = 0 (No Correlation)"):
            st.markdown("""
                **Interpretation:** No linear relationship between the two variables. Changes in one variable do not systematically relate to changes in the other.
            """)

    with col7:
        with st.expander("r = -0.3 ≤ r < 0 (Weak Negative Correlation)"):
            st.markdown("""
                **Interpretation:** A weak negative relationship. As one variable increases, the other decreases, but the relationship is weak.
            """)

    with col8:
        with st.expander("r = -0.7 ≤ r < -0.3 (Moderate Negative Correlation)"):
            st.markdown("""
                **Interpretation:** A moderate negative relationship. As one variable increases, the other decreases in a somewhat linear fashion.
            """)

    # Scatter plot with trendline
    fig = px.scatter(
        filtered_corr_data,
        x="DEPTH",
        y="MAG",
        labels={"DEPTH": "Depth (km)", "MAG": "Magnitude"},
        title="Filtered Depth vs Magnitude",
        trendline="ols",
        opacity=0.7
        )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.info("Tip: Use sidebar filters (if available) on other pages to explore more detailed data views.")



