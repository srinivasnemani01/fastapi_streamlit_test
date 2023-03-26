import streamlit as st
from gui.data_uploader import DataUploadPage
from gui.data_analysis import DataAnalysisPage


# Set page title and layout
st.set_page_config(page_title="Market data analysis", layout="wide")

# Define dictionary of tab names and corresponding classes
tab_gui_mapping = {
    "Upload data": DataUploadPage,
    "Data analysis": DataAnalysisPage
}

# Get current tab selection
current_tab = st.sidebar.radio("Select a tab", list(tab_gui_mapping.keys()))
if "session_count" not in st.session_state:
    st.session_state["current_tab"] = current_tab

# Instantiate class based on current tab selection
data_analysis_page = tab_gui_mapping[current_tab]("config.ini", st.session_state)
data_analysis_page.render_the_page()
