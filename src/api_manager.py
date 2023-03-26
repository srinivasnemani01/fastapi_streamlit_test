from sqlalchemy import create_engine, text
from fastapi import FastAPI, UploadFile, File, HTTPException
from dbutil.optiondata_dao import DataPersistenceORM, DataPersistence
from dbutil.dbschema import BrentOptionData, get_optiondata_dbschmea
import pandas as pd
from typing import Optional, List
import datetime
from api.optionadata_fetcher import OptionDataFetcher
from api.optionadata_uploader import OptionDataUploader
from api.option_pricer import OptionPricer
import uvicorn
import configparser

class APIManager:
    def __init__(self, ini_path: str):
        config = configparser.ConfigParser()
        config.read(ini_path)

        # create the engine and database
        sql_server = 'sqlite:///'
        db_name = config['DATABASE']['sqlite_file']
        database_url = sql_server + db_name
        optiondata_dbschmea = get_optiondata_dbschmea()
        
        # create the FastAPI instance and data persistence object
        self.app = FastAPI()
        
        self.persistence = DataPersistenceORM(database_url)

        # create the table if it does not exist
        print("calling the creation of tables...")
        self.persistence.create_table(optiondata_dbschmea)

        self.uploader = OptionDataUploader(self.persistence)
        self.fetcher = OptionDataFetcher(self.persistence)
        self.calculator = OptionPricer(self.persistence)

        self.initialize_api_endpoints()

        # read the API host and port from the config file
        self.host = config['API']['host']
        self.port = int(config['API']['port'])

    def initialize_api_endpoints(self):
        self.app.post("/loadmarketdatajson")(self.uploader.load_market_data_json)
        self.app.post("/loadmarketdatafile")(self.uploader.load_market_data_file)
        self.app.post("/loadmarketdatastreaming")(self.uploader.load_market_data_iostream)
        self.app.get("/fetchdata_asof/{date_as_of}")(self.fetcher.fetch_records_asof)
        self.app.get("/fetchuniqutedates/")(self.fetcher.fetch_distinct_dates)
        self.app.get("/calculateoptionprices/{date_as_of}/")(self.calculator.calculate_market_prices)

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host=self.host, port=self.port)

if __name__ == "__main__":
    CONFIG_FILE = 'config.ini'
    api_manager = APIManager(CONFIG_FILE)       
    api_manager.run()
