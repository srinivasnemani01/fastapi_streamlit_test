from fastapi import FastAPI, HTTPException
from dbutil.optiondata_dao import DataPersistenceORM
from dbutil.dbschema import get_optiondata_dbschmea
import pandas as pd
from typing import Optional, List
import configparser
from api.optionadata_fetcher import OptionDataFetcher
from api.optionadata_uploader import OptionDataUploader
from api.option_pricer import OptionPricer

"""
    This module acts the API end point manager responsible for
    initializing endpoints, and handling incoming requests. 
    
    The managr class named "APIManager" utilizes the OptionDataFetcher, OptionDataUploader, 
    and OptionPricer classes to provide functionalities for 
    uploading, fetching, and calculating option prices.

    The APIManager class reads the configuration file, sets up the 
    FastAPI application and persistence object, and initializes API endpoints.
    It runs the FastAPI application with the specified host and port.

"""

class APIManager:
    """
        This class contains methods for setting the required endpoints based on the configurations file 
        such as host address, ports, initializing API endpoints using the give URLs.
    """
    
    def __init__(self, ini_path: str):
        """
        Initializes the APIManager with the given configuration file.
        Args:
            ini_path (str): The path to the configuration file.
        """
        print("api manager starting..")
        config = configparser.ConfigParser()
        config.read(ini_path)

        # create the engine and database
        sql_engine = 'sqlite:///'
        db_name = config['DATABASE']['sqlite_file']
        database_url = sql_engine + db_name
        optiondata_dbschmea = get_optiondata_dbschmea()
        
        # create the FastAPI instance and data persistence object
        self.app = FastAPI()
        
        self.persistence = DataPersistenceORM(database_url)
        self.persistence.create_table(optiondata_dbschmea)
        
        self.uploader = OptionDataUploader(self.persistence)
        self.fetcher = OptionDataFetcher(self.persistence)
        self.calculator = OptionPricer(self.persistence)

        self.initialize_api_endpoints()

        # read the API host and port from the config file
        self.host = config['API']['host']
        self.port = int(config['API']['port'])

    def initialize_api_endpoints(self) -> None:
        """
        Initializes the API endpoints for the application.
        """
        self.app.post("/loadmarketdatajson")(self.uploader.load_market_data_json)
        self.app.post("/loadmarketdatafile")(self.uploader.load_market_data_file)
        self.app.post("/loadmarketdatastreaming")(self.uploader.load_market_data_iostream)
        self.app.get("/fetchdata_asof/{date_as_of}")(self.fetcher.fetch_records_asof)
        self.app.get("/fetchuniqutedates/")(self.fetcher.fetch_distinct_dates)
        self.app.get("/calculateoptionprices/{date_as_of}/")(self.calculator.calculate_market_prices)

    def run(self) -> None:
        """
        Runs the FastAPI application with the specified host and port.
        """
        import uvicorn
        uvicorn.run(self.app, host=self.host, port=self.port)

if __name__ == "__main__":
    CONFIG_FILE = 'config.ini'
    api_manager = APIManager(CONFIG_FILE)       
    api_manager.run()
