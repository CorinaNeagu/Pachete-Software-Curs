import streamlit as st
import importlib

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found, using default styles.")

# Load the custom CSS
load_css("app.css")

# App Header
st.markdown("<h1 style='text-align: center;'>🌍 Earthquake Visualizer</h1>", unsafe_allow_html=True)
st.markdown("<h2>Navigate to a section:</h2>", unsafe_allow_html=True)

# --- Initialize Session ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- Custom Button Layout ---
buttons = [
    ("📈 Statistics", 'descriptiveStat'),
    ("📊 Heat Map", 'heatMap'),
    ("🌵 Spike Map", 'bubbleMap'),
    ("🎞️ Animated Map", 'animatedMap'),
    ("🔁 Flow Map", 'flowMap')
]

# --- Button Container ---
cols = st.columns(len(buttons))
for col, (label, target_page) in zip(cols, buttons):
    with col:
        if st.button(f" {label} ", key=label):
            st.session_state.page = target_page  
            st.rerun()  # Trigger a rerun of the app after button press

# --- Page Loader ---
pages = {
    "bubbleMap": "bubbleMap",
    "heatMap": "heatMap",
    "animatedMap": "animatedMap",
    "descriptiveStat": "descriptiveStat",
    "flowMap": "flowMap"
}

def load_page(page_name):
    try:
        # Dynamically load the module and run it
        module = importlib.import_module(pages[page_name])
        module.run()
    except Exception as e:
        st.error(f"🚨 Error loading `{page_name}`: {e}")

# --- Route to Page ---
if 'clear_content' not in st.session_state:
    st.session_state.clear_content = False

# If the page is changed, reset the placeholder (clear content)
if st.session_state.clear_content:
    st.empty()
    st.session_state.clear_content = False  # Reset the flag

# --- Route to the selected page ---
if st.session_state.page in pages:
    st.session_state.clear_content = True
    load_page(st.session_state.page)
