from fastapi import FastAPI, UploadFile, File, HTTPException
from dbutil.dbschema import BrentOptionData
from dbutil.optiondata_dao import DataPersistence, DataPersistenceORM
from typing import Optional, List
from fastapi.responses import JSONResponse
from models.b76_model import B76OptionPricer

class OptionPricer:
    def __init__(self, persistence: DataPersistence):
        self.persistence = persistence
        
    async def calculate_market_prices(self, date_as_of: int):
        query = (BrentOptionData.DateAsOf == date_as_of,)
        fetched_data = self.persistence.fetch_records(BrentOptionData, query)
        option_pricer = B76OptionPricer(fetched_data)
        option_prices = option_pricer.calculate_option_prices()
        
        json_str = fetched_data.to_json(orient="records")
        return JSONResponse(content={"success": json_str})
