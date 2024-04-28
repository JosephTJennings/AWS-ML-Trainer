from sqlalchemy import create_engine, MetaData, Table, select, column
import pandas as pd

db_url = "mysql+mysqlconnector://admin:password@mltrainerdb.cbeowqykkubi.us-east-2.rds.amazonaws.com:3306/MLdatasets"
username = "admin"
password = "password"
fields = ["optionsExpire", "strikePrice", "volume", "delta", "gamma", "iv", "rho"]
table_name = "options"

engine = create_engine(db_url, connect_args={'user': username, 'password': password})
conn = engine.connect()

metadata = MetaData()

# Reflect the existing database schema into the MetaData object
metadata.reflect(bind=engine)

options_table = metadata.tables[table_name]

# Build the select statement using individual columns
columns = [options_table.c[field] for field in fields]
stmt = select(*columns)

# Execute the query
result = conn.execute(stmt)

# Fetch the results into a DataFrame
data = pd.DataFrame(result.fetchall(), columns=fields)
print(data)
# Close the connection
conn.close()

# Now you have your data in the 'data' DataFrame
