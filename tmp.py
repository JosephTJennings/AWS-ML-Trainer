from sqlalchemy import create_engine, MetaData, Table, select, column
import pandas as pd

def query_database(db_url, username, password, fields, table):
    # Create SQLAlchemy engine with username and password
    constr_url = "mysql+mysqlconnector://" + username + ":" + password + "@" + db_url
    engine = create_engine(constr_url, connect_args={'user': username, 'password': password})
    
    # Reflect the existing database schema into the MetaData object
    metadata = MetaData()
    metadata.reflect(bind=engine)
    target_table = metadata.tables[table]

    # Build the select statement using individual columns
    columns = [target_table.c[field.strip()] for field in fields.split(',')]
    stmt = select(*columns)

    # Fetch data using SQLAlchemy
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            data = pd.DataFrame(result.fetchall(), columns=[c.name for c in columns])
    except Exception as e:
        raise e
    
    return data
def main():
    db_url = "mltrainerdb.cbeowqykkubi.us-east-2.rds.amazonaws.com:3306/MLdatasets"
    username = "admin"
    password = "password"
    fields = "optionsExpire,strikePrice,volume,delta,gamma,iv,rho"
    table_name = "options"
    print(query_database(db_url, username, password, fields, table_name))

# Now you have your data in the 'data' DataFrame
main()