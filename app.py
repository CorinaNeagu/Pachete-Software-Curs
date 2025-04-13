import streamlit as st

# Initialize session state for page navigation if it doesn't exist
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# Landing page
if st.session_state.page == 'landing':
    st.title("Choose a page to navigate to:")

    # Buttons to navigate to different pages
    if st.button("See Heat Map"):
        st.session_state.page = 'mapping'  

    if st.button("See Bubble Map"):
        st.session_state.page = 'bubbleMap'  

    if st.button("See Statistics"):
        st.session_state.page = 'otherPage'

    if st.button("See Animated Map"):
        st.session_state.page = 'animatedMap'

# Bubble Map Page
elif st.session_state.page == 'bubbleMap':
    try:
        import bubbleMap
        bubbleMap.run()
    except Exception as e:
        st.error(f"Error loading Bubble Map: {e}")

# Heat Map Page (Mapping)
if st.session_state.page == 'mapping':
    try:
        import heatMap
        heatMap.run()
    except Exception as e:
        st.error(f"Error loading Heat Map: {e}")

elif st.session_state.page == 'animatedMap':
    try:
        import animatedMap
        animatedMap.run()
    except Exception as e:
        st.error(f"Error loading Animated Map: {e}")

# Statistics Page
elif st.session_state.page == 'otherPage':
    try:
        import otherPage
        otherPage.run()
    except Exception as e:
        st.error(f"Error loading Statistics: {e}")
