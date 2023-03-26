import configparser
import streamlit as st
from gui.data_uploader import DataUploadPage
from gui.data_analysis import DataAnalysisPage

class MarketDataAnalysisApp:
    def __init__(self, config):
        self.config = config
        st.set_page_config(page_title="Market data analysis", layout="wide")

    def run(self):
        tab_gui_mapping = {
            "Upload data": DataUploadPage,
            "Data analysis": DataAnalysisPage
        }

        current_tab = st.sidebar.radio("Select a tab", list(tab_gui_mapping.keys()))
        if "session_count" not in st.session_state:
            st.session_state["current_tab"] = current_tab

        data_analysis_page = tab_gui_mapping[current_tab](self.config, st.session_state)
        data_analysis_page.render_the_page()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    CONFIG_FILE = 'config.ini'
    app = MarketDataAnalysisApp(CONFIG_FILE)
    app.run()    