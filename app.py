import streamlit as st
import importlib

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found, using default styles.")

# Custom CSS
load_css("app.css")

# App Header
st.markdown("<h1 style='text-align: center;'>🌍 Earthquake Visualizer</h1>", unsafe_allow_html=True)
st.markdown("<h2>Navigate to a section:</h2>", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'landing'

buttons = [
    ("📈 Statistics", 'descriptiveStat'),
    ("📊 Heat Map", 'heatMap'),
    ("🌵 Spike Map", 'spikeMap'),
    ("🎞️ Animated Map", 'animatedMap'),
    ("🔁 Flow Map", 'flowMap')
]

cols = st.columns(len(buttons))
for col, (label, target_page) in zip(cols, buttons):
    with col:
        if st.button(f" {label} ", key=label):
            st.session_state.page = target_page  
            st.rerun() 

pages = {
    "spikeMap": "spikeMap",
    "heatMap": "heatMap",
    "animatedMap": "animatedMap",
    "descriptiveStat": "descriptiveStat",
    "flowMap": "flowMap"
}

def load_page(page_name):
    try:
        module = importlib.import_module(pages[page_name])
        module.run()
    except Exception as e:
        st.error(f" Error loading `{page_name}`: {e}")

if 'clear_content' not in st.session_state:
    st.session_state.clear_content = False

if st.session_state.clear_content:
    st.empty()
    st.session_state.clear_content = False  

if st.session_state.page in pages:
    st.session_state.clear_content = True
    load_page(st.session_state.page)
