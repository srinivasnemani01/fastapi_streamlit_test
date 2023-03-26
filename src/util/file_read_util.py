import configparser
import requests
import streamlit as st
import datetime
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from typing import Set

class DataProcessingUtilities():
    @staticmethod
    def validate_header(option_data: pd.DataFrame, required_columns: Set[str]) -> None:
        if set(option_data.columns) != required_columns:
            error_message = "The uploaded file does not contain all required columns. Required columns: " + ", ".join(required_columns)
            raise ValueError(error_message)
  
    @staticmethod
    def validate_file_type(filename):
        if filename.endswith('.csv'):
            option_data = pd.read_csv(filename)
        elif filename.endswith('.xlsx'):
            option_data = pd.read_excel(filename)
        else:
            raise ValueError("Invalid file format. Please upload a CSV or Excel file.")

            
    @staticmethod
    def convert_value_error_to_http_error(e: ValueError) -> HTTPException:
        error_message = str(e)
        return HTTPException(status_code=400, detail=error_message)

    @staticmethod
    def read_file(filename):
        DataProcessingUtilities.validate_file_type(filename)
        print("In the read file of Option Data Validation Class....")
        with open(filename, 'rb') as file:
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.csv':
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        return df