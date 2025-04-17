import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Your MySQL username
        password='nikunjjain2005@SQL',  # Your MySQL password
        database='auctiondb'  # The database you're using
    )
    return connection
