# Python Project: Data Transfer from On-Premises SQL Server to Azure SQL

## Overview
This project contains a Python script that facilitates the transfer of data from an on-premises SQL Server database to an Azure SQL database. The script connects to both databases, retrieves data from specified tables, and uploads it to Azure SQL using the pandas and SQLAlchemy libraries.

## Prerequisites
Before running the script, ensure you have the following installed:
- Python 3.x
- Required Python packages:
  - `pandas`
  - `pyodbc`
  - `sqlalchemy`

You can install the required packages using pip:

```
pip install pandas pyodbc sqlalchemy
```

## Configuration
1. Update the connection strings in `src/databricks_onprem_to_azure_sql.py` with your on-premises and Azure SQL database credentials:
   - `ONPREM_SERVER`
   - `ONPREM_DB`
   - `ONPREM_USER`
   - `ONPREM_PASSWORD`
   - `AZURE_USER`
   - `AZURE_PASSWORD`
   - `AZURE_SERVER`
   - `AZURE_DB`

2. Specify the tables you want to transfer in the `tables_to_transfer` list within the script.

## Running the Script
To execute the data transfer, run the following command in your terminal:

```
python src/databricks_onprem_to_azure_sql.py
```

## Notes
- Ensure that the ODBC Driver 17 for SQL Server is installed on your machine.
- The script will replace existing tables in the Azure SQL database with the transferred data. Adjust the `if_exists` parameter in the `to_sql` method if you want to change this behavior.

## License
This project is licensed under the MIT License.