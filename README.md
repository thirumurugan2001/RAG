RAG System for Famous Places in India

Overview

This project implements a Retrieval-Augmented Generation (RAG) system using FastAPI, SingleStore, and Cohere embeddings. It allows users to query information about famous places in India and retrieve the most relevant answers based on vector similarity.

Features

FastAPI-based RESTful API

Cohere API for generating text embeddings

SingleStore for storing and querying vector data

Excel data ingestion for batch uploads

Technologies Used

Python 3.8+

FastAPI for API development

Cohere for text embeddings

SingleStore (MemSQL) for vector storage and retrieval

Pandas for Excel data handling

Uvicorn as the ASGI server

dotenv for environment variable management

Setup Instructions

Clone the Repository
https://github.com/thirumurugan2001/RAG.git
cd rag

Install Dependencies
pip install -r requirements.txt

Configure Environment Variables
Create a .env file in the root directory:
API_KEY=your_cohere_api_key
Hostsvc=your_singlestore_host
Port=your_singlestore_port
User_name=your_db_username
Password=your_db_password
Database=your_database_name

Prepare the Database

Ensure SingleStore is running.

Run the CreateTable function to create the necessary table:
from your_module import CreateTable
CreateTable()

Insert Data
Ensure Famous_Places_India.xlsx is in the project directory, then run:
from your_module import insert_into_database
insert_into_database()

Run the API
uvicorn main:app --host 0.0.0.0 --port 8000

API Usage

Endpoint: POST /rag/

Request Body:
{
"Question": "Tell me about the Taj Mahal"
}

Response:
{
"data": "Taj Mahal",
"statusCode": 200
}

File Structure

main.py            - FastAPI application
controller.py      - Handles API logic
rag.py             - Core RAG functionality
Helper.py          - Database and embedding helpers
.env               - Environment variables
requirements.txt   - Python dependencies
Famous_Places_India.xlsx  - Data source

Troubleshooting

Database Connection Issues: Verify .env settings.

API Errors: Check logs for error messages.

Data Insertion Failures: Ensure the Excel file is formatted correctly.

License
MIT License

Acknowledgements

Cohere: https://cohere.ai/

SingleStore: https://www.singlestore.com/

FastAPI: https://fastapi.tiangolo.com/