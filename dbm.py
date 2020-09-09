import pandas as pd
import sqlite3
from sqlalchemy import create_engine

data = pd.read_excel("demofile_deleteit.xlsx")


#SAVE DATAFRAME TO SQLLITE

engine = create_engine('sqlite:///save_transaction_new.db', echo=True)
        
sqlite_connection = engine.connect()
sqlite_table = "customer_transaction"
data.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
sqlite_connection.close()