from abc import ABC, abstractmethod
import configparser
import requests
import streamlit as st
import pandas as pd
from typing import Optional

class IOptionPricer(ABC):
    def __init__(self, market_data: pd.DataFrame):
        self.model_name = 'Black76'
        self.market_data = market_data

    @abstractmethod
    def calculate_option_prices(self):
        pass
