import pyodbc
import pandas as pd
from sqlalchemy import create_engine

# Securely fetch credentials using Databricks secrets
username = dbutils.secrets.get(scope="netsuite-secrets", key="sv-sql-01-uname")
password = dbutils.secrets.get(scope="netsuite-secrets", key="sv-sql-01-pword")

# On-premises database connection details
onprem_conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER=ONPREM_SERVER;"
    f"DATABASE=ONPREM_DB;"
    f"UID={username};"
    f"PWD={password};"
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

chunksize = 10000  # Adjust chunk size as needed

for schema, table in tables_to_transfer:
    query = f"SELECT * FROM [{schema}].[{table}]"
    first_chunk = True
    for chunk in pd.read_sql(query, onprem_conn, chunksize=chunksize):
        chunk.to_sql(
            name=table,
            con=azure_engine,
            schema=schema,
            if_exists='replace' if first_chunk else 'append',
            index=False
        )
        first_chunk = False
        print(f"Transferred chunk of {schema}.{table} to Azure SQL.")

onprem_conn.close()
azure_engine.dispose()