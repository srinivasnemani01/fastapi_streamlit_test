from dbutil.dbschema import BrentOptionData
from dbutil.optiondata_dao import DataPersistence
import pandas as pd
from fastapi.responses import JSONResponse

class OptionDataFetcher:
    def __init__(self, persistence: DataPersistence):
        self.persistence = persistence

    async def fetch_records_asof(self, date_as_of: int):
        query = (BrentOptionData.DateAsOf == date_as_of,)
        fetched_data = self.persistence.fetch_records(BrentOptionData, query)
        json_str = fetched_data.to_json(orient="records")
        return JSONResponse(content={"success": json_str})

    async def fetch_distinct_dates(self):
        query = (BrentOptionData.DateAsOf,)
        fetched_data = self.persistence.fetch_records(BrentOptionData, query)
        unique_dates = fetched_data["DateAsOf"].unique()

        # Convert the unique_dates Series to a JSON string and return it.
        json_str = pd.Series(unique_dates).to_json(orient="values")
        return JSONResponse(content={"success": json_str})
