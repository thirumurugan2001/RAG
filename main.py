from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from controller import *
app = FastAPI()


class Item(BaseModel):
    Question: str

# API to get the most relevant answer from the database
@app.post("/rag/")
async def rag(item: Item):
    try :
        response = ragController(item.Question)
        return response
    except Exception as e:
        return {
            "error": str(e),
            "stratusCode": 500
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)