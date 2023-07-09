import pymssql 
import pandas as pd
from db_connect_helpers import readin_csv
from db_connect_helpers import retrieve_telephones, retrieve_emails
from db_connect_helpers import insert_company_entry, insert_telephone_entry, insert_email_entry

DATABASE = 'isbu_db'
USERNAME = 'sa'
PASSWORD = 'reallyStrongPwd123'
 
# Create a connection
conn = pymssql.connect(server = '10.3.128.85', 
                      user = USERNAME,
                      password = PASSWORD,
                      database = DATABASE)

print(" CONNECTED TO DB SUCCESFULLY")

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