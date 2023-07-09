import pymssql 
import pandas as pd
from db_connect_helpers import readin_csv
from db_connect_helpers import retrieve_telephones, retrieve_emails
from db_connect_helpers import insert_company_entry, insert_telephone_entry, insert_email_entry

DATABASE = 'isbu_db'
USERNAME = 'sa'
PASSWORD = 'reallyStrongPwd123'

df = readin_csv('infosecindex.csv')
df = df
# company_df, telephone_df, email_df = separate_dfs(df)
 
conn = pymssql.connect(server = '10.3.128.85', 
                      user = USERNAME,
                      password = PASSWORD,
                      database = DATABASE)

print(" CONNECTED TO DB SUCCESFULLY")