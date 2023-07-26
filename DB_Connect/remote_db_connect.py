import pyodbc
import pandas as pd
from db_connect_helpers import readin_csv
from db_connect_helpers import retrieve_telephones, retrieve_emails
from db_connect_helpers import insert_company_entry, insert_telephone_entry, insert_email_entry

DATABASE = 'isbu_db'
USERNAME = 'sa'
PASSWORD = 'reallyStrongPwd123'
 

# Establish a connection using the ODBC driver and connection string
conn = pyodbc.connect(
    driver='{ODBC Driver 18 for SQL Server}',  # Replace with the appropriate ODBC driver name
    server='194.90.46.138',  # Replace with the server name or IP address of your MSSQL Edge server
    database=DATABASE,  # Replace with the name of your database
    uid=USERNAME,  # Replace with your username
    pwd=PASSWORD  # Replace with your password
)


# # Create a connection
# conn = pymssql.connect(server = '194.90.46.138', 
#                       user = USERNAME,
#                       password = PASSWORD,
#                       database = DATABASE)

# print(" CONNECTED TO DB SUCCESFULLY")

# Create a cursor object
cursor = conn.cursor()

# Execute the query
trial_query = "SELECT * FROM Company;"
cursor.execute(trial_query)

# Fetch all rows from the result
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the cursor and the connection
cursor.close()
conn.close()