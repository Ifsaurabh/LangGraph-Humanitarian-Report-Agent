# imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import TypedDict
import uvicorn
from agent.graph import app as aga

# App
app = FastAPI(title="Autonomous Humanitarian Report Generator")

# pydantic model
class QueryRequest(BaseModel):
    question: str
    
class QueryResponse(BaseModel):
    answer: str
    

@app.post("/question",  response_model=QueryResponse)
def get_report(request: QueryRequest):
    final_report = aga.invoke({"question": request.question})
    return {"answer": final_report['final_report']}

if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)