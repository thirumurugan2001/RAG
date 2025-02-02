from ast import arg
import os
from openai import OpenAI
import singlestoredb as s2
from dotenv import load_dotenv
import pandas as pd
import numpy as np
load_dotenv()

# Function to get the embedding of the text
def get_embedding(text):
    try:
        token = token = os.getenv("KEY")
        endpoint = "https://models.inference.ai.azure.com"
        model_name = "text-embedding-3-large"

        client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )
        response = client.embeddings.create(
            input=[text],
            model=model_name,
        )
        return response.data[0].embedding
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

def read_excel_file():
    try:
        file_path=r'Famous_Places_India.xlsx'
        df = pd.read_excel(file_path)
        print("Excel file read successfully")
        return df
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None

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
        conn.commit()
    except Exception as e:
        print("Error in inserting data:", str(e))
        return None

# select_query= **"select name, dot product(vector, JSON_ARRAY PACK("{0}")) as score from explore_it order by score desc limit 1***.format(embedding) 
# print("Query: "+select_query) 
# cur.execute(select_query) 
# rows = cur.fetchall() 
# for row in rows: 
# print(row)

print(insert_into_database())

