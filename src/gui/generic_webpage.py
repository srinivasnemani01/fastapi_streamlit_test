from abc import ABC, abstractmethod
import configparser
import requests
import streamlit as st

class IWebPage(ABC):
    def __init__(self, config_file, session_state):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.session_state = session_state

    @abstractmethod
    def render_the_page(self):
        pass
        