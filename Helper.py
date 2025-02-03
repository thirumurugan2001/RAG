from ast import arg
import os
import singlestoredb as s2
from dotenv import load_dotenv
import pandas as pd
import cohere
load_dotenv()

# Function to get the embedding of the text
def get_embedding(text):
    try:
        token = os.getenv("API_KEY")
        co = cohere.Client(token)  
        embedding = co.embed(
            model='embed-english-v3.0', 
            input_type='classification', 
            texts=[text]
            ).embeddings[0] 
        return embedding
    except Exception as e:
        print("Error in getting embedding: ", str(e))
        return None
    
# Function to connect to SingleStore
def dbconnection():
    try :
        conn = s2.connect( 
            host = os.getenv("Hostsvc"), 
            port = os.getenv("Port"), 
            user =os.getenv("User_name"), 
            password = os.getenv("Password") , 
            database =  os.getenv("Database")
        )
        print("Connected to SingleStore")
        return conn
    except Exception as e:
        print("Error in connecting to SingleStore: ", str(e))
        return None
    
# Function to create a table in SingleStore
def CreateTable():
    try:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE famousPlacesIndia (place TEXT, description TEXT,vector blob);")
        conn.commit()
        return "Table created successfully"
    except Exception as e:
        print("Error in creating table: ", str(e))
        return None

# Function to select data into SingleStore
def selectData():
    try:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM famous_places")
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("Error in selecting data: ", str(e))
        return None
    
# Function to select data into SingleStore
def dropTable():
    try:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE famousPlacesIndia")
        conn.commit()
        return "Table dropped successfully"
    except Exception as e:
        print("Error in selecting data: ", str(e))
        return None

# Function to read the excel file
def read_excel_file():
    try:
        file_path=r'Famous_Places_India.xlsx'
        df = pd.read_excel(file_path)
        print("Excel file read successfully")
        return df
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None

# Function to insert data into the database
def insert_into_database():
    try:
        conn = dbconnection()
        df = read_excel_file()
        cursor = conn.cursor()
        for index, row in df.iterrows():
            place = row['Place']
            description = row['Description']
            vector = get_embedding(description)
            query = """insert into famousPlacesIndia (place, description, vector) values ("{0}", "{1}", JSON_ARRAY_PACK("{2}"))""".format(place, description, vector)
            cursor.execute(query)
        return "Data inserted successfully"
    except Exception as e:
        print("Error in inserting data:", str(e))
        return None