import pyodbc
import pandas as pd
from sqlalchemy import create_engine

# On-premises database connection details
onprem_conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=ONPREM_SERVER;"
    "DATABASE=ONPREM_DB;"
    "UID=ONPREM_USER;"
    "PWD=ONPREM_PASSWORD;"
)

# Azure SQL database connection details
azure_conn_str = (
    "mssql+pyodbc://AZURE_USER:AZURE_PASSWORD@AZURE_SERVER/AZURE_DB"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

# List of (schema, table) tuples to transfer
tables_to_transfer = [
    ("schema1", "table1"),
    ("schema2", "table2"),
    ("schema3", "table3"),
]

# Connect to on-premises database
onprem_conn = pyodbc.connect(onprem_conn_str)

# Create SQLAlchemy engine for Azure SQL
azure_engine = create_engine(azure_conn_str, fast_executemany=True)

for schema, table in tables_to_transfer:
    query = f"SELECT * FROM [{schema}].[{table}]"
    df = pd.read_sql(query, onprem_conn)
    df.to_sql(
        name=table,
        con=azure_engine,
        schema=schema,
        if_exists='replace',
        index=False
    )
    print(f"Transferred {schema}.{table} to Azure SQL.")

onprem_conn.close()
azure_engine.dispose()