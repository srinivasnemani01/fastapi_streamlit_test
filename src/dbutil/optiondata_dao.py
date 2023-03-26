from sqlalchemy import create_engine, and_
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod
import pandas as pd
import os
import datetime

Base = declarative_base()

class DataPersistence(ABC):

    @abstractmethod
    def create_table(self, table_class: Base):
        pass

    @abstractmethod
    def add_records(self, table_class: Base, data: pd.DataFrame):
        pass

    @abstractmethod
    def fetch_records(self, table_class: Base, query):
        pass

    @abstractmethod
    def delete_records(self, table_class: Base, query):
        pass

    @abstractmethod
    def update_records(self, table_class: Base, query, update_data):
        pass
        
        
class DataPersistenceORM(DataPersistence):
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_table(self, table_class: Base):
        #os.system('cls||clear')
        Base.metadata.create_all(self.engine)

    def add_records(self, table_class: Base, data: pd.DataFrame):
        session = self.Session()
        try:
            data.to_sql(table_class.__tablename__, self.engine, if_exists='replace', index=False)
            ct = datetime.datetime.now()  

        except Exception as err_msg:
            raise ValueError(f"Error adding records: {err_msg}")
        finally:
            session.commit()
            session.close()

    def fetch_records(self, table_class: Base, query=None):
        try:
            session = self.Session()			
            ct = datetime.datetime.now()

            with self.Session() as session:
                if isinstance(query, str):
                    records = session.query(table_class).filter(text(query))                   
                else:
                    records = session.query(table_class).filter(and_(*query)).all()
            records_dict = [record.__dict__ for record in records]

            for record in records_dict:
                record.pop('_sa_instance_state', None)
				
            df = pd.DataFrame(records_dict)
            return df

        except Exception as err_msg:
            ct = datetime.datetime.now()    
            raise ValueError(f"Error adding records: {err_msg}")
        finally:
            session.commit()
            session.close()

    def delete_records(self, table_class: Base, query):
        session = self.Session()
        try:
            session.query(table_class).filter(and_(*query)).delete()
            session.commit()
        except Exception as err_msg:
            raise ValueError(f"Error deleting records: {err_msg}")
        finally:        
            session.close()

    def update_records(self, table_class: Base, query, update_data):
        session = self.Session()
        try:
            session.query(table_class).filter(and_(*query)).update(update_data)
            session.commit()
        except Exception as err_msg:
            raise ValueError(f"Error updating records: {err_msg}")
        finally:
            session.close()       
