from fastapi import UploadFile, HTTPException, File, Header, Request
from pydantic import BaseModel
from dbutil.dbschema import BrentOptionData
from dbutil.optiondata_dao import DataPersistence, DataPersistenceORM
import pandas as pd
from util.file_read_util import DataProcessingUtilities
import io
import json
from typing import Optional
import gzip
import os
from typing import List

REQUIRED_COLUMNS = {'DateAsOf', 'FutureExpiryDate', 'OptionType', 'StrikePrice', 'CurrentPrice', 'ImpliedVol'}

class MarketDataPydantic(BaseModel):
    DateAsOf: Optional[int]
    FutureExpiryDate: Optional[int]
    OptionType: Optional[str]
    StrikePrice: Optional[float]
    CurrentPrice: Optional[float]
    ImpliedVol: Optional[float]


class MarketDataList(BaseModel):
    data: List[MarketDataPydantic]

column_names = ['DateAsOf', 'FutureExpiryDate', 'OptionType', 'StrikePrice', 'CurrentPrice', 'ImpliedVol']

class OptionDataUploader:
    def __init__(self, persistence: DataPersistence):
        self.persistence = persistence

    async def load_market_data_json(self, market_data_list: MarketDataList):
        os.system('cls' if os.name == 'nt' else 'clear')
        item = market_data_list.data
        df = pd.DataFrame(item, columns=column_names)
        for column in column_names:
            df[column] = df[column].apply(lambda x: x[1])

        self.persistence.add_records(BrentOptionData, df)
        return {"success": "Json market data uploaded to database."}

    async def load_market_data_file(self, file: UploadFile):
        try:
            DataProcessingUtilities.validate_file_type(file.filename)
            market_data_df = DataProcessingUtilities.read_file(file.filename)
            DataProcessingUtilities.validate_header(market_data_df, REQUIRED_COLUMNS)
        except ValueError as e:
            DataProcessingUtilities.convert_value_error_to_http_error(ValueError)

        self.persistence.add_records(BrentOptionData, market_data_df)
        return {"success": "Market data from the given file uploaded successfully."}

    async def load_market_data_iostream(self, request: Request, content_encoding: str = Header(None)):
        try:
            if content_encoding == "gzip":
                compressed_data = io.BytesIO(file)
                market_data = gzip.open(compressed_data, "rb")
            else:
                market_data = io.BytesIO(file).getvalue()
        except ValueError as e:
            DataProcessingUtilities.convert_value_error_to_http_error(ValueError)
        return {"success": "gzip or iostream file is processed."}
