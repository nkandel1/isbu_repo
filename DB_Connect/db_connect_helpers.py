import pymssql 
import pandas as pd

# Reads in CSV, removes extra first row and fills NaNs with empty string
def readin_csv(file_name):
    df = pd.read_csv(file_name)

    df = df.drop(['Unnamed: 0'],axis=1)
    df = df.drop(df.index[0]).reset_index(drop=True).fillna('')

    return df

# Input telephone string (that looks like a list), returns a list of telephones
# Ex. Input = "['+1 (646) 715-4483', '0559879663']", return = ['+1 (646) 715-4483', '0559879663']
def retrieve_telephones(telephone_string):
    telephone_lst = [s.strip("' ") for s in telephone_string.strip("[]").split(",") if s.strip("' ")]
    return telephone_lst


# Input email string (that looks like a list), returns a list of telephones
# Ex. Input = "[silvia@gmail.com', 'isbu@isbu.com']", return = [silvia@gmail.com', 'isbu@isbu.com']
def retrieve_emails(email_string):
    email_lst = [s.strip("' ") for s in email_string.strip("[]").split(",") if s.strip("' ")]
    return email_lst


def insert_company_entry(company_name, company_tagline, website, conn, cursor):
    try:
        # INSERT A COMPANY ENTRY
        company_data = (company_name,company_tagline, website)
        query_insert = "INSERT INTO Company (company_name, company_tagline, website) VALUES (%s, %s, %s);"
        cursor.execute(query_insert, company_data)

        # Retrieve the last generated company_id
        query_company_id = "SELECT SCOPE_IDENTITY() AS last_company_id;"
        cursor.execute(query_company_id)

        last_company_id = cursor.fetchone()[0]

        # Commit the transaction
        conn.commit()   
    
    except pymssql.DatabaseError as e:
        # Check if the error message matches Duplicate key violation
        error_message = str(e)

        # If company_name is repeated, don't re-eneter it, but grab the company_id to add Telephone and Email info
        if "Violation of UNIQUE KEY constraint" in error_message:
            print("Duplicate key violation occurred:", error_message)

            query_company_id = "SELECT company_id FROM Company WHERE company_name = (%s);"
            cursor.execute(query_company_id, company_name)

            last_company_id = cursor.fetchone()[0]

        else:
            print("DatabaseError occurred:", error_message)

    return last_company_id

def insert_telephone_entry(telephone, company_id, conn, cursor):

    # From the telephone string, retrieve the individual telephones (still as strings)
    telephones = retrieve_telephones(telephone)

    # If telephone list isn't empty, add entries to Telephones table, with foreign key last_company_id
    if telephones:
        for t in telephones:
            telephone_data = (t, company_id)
            query = " INSERT INTO Telephone (telephone, company_id) VALUES  (%s, %s);" 
            cursor.execute(query, telephone_data)
    
    # Commit the transactions
    conn.commit()  

def insert_email_entry(email, company_id, conn, cursor):
    
    # From the email string, retrieve the individual emails (still as strings)
    emails = retrieve_emails(email)

    # If email list isn't empty, add entries to Email table, with foreign key last_company_id
    if emails:
        for e in emails:
            email_data = (e, company_id)
            query = "INSERT INTO Email (email, company_id) VALUES  (%s, %s);"  
            cursor.execute(query, email_data)

    # Commit the transactions
    conn.commit()  
