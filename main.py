

# imports
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import TypedDict
import uvicorn
from agent.graph import app as aga
import anthropic
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os
from dotenv import load_dotenv


load_dotenv()

# security
security = HTTPBasic()
correct_username = os.getenv("BASIC_AUTH_USERNAME")
correct_password = os.getenv("BASIC_AUTH_PASSWORD")

# App
app = FastAPI(title="Autonomous Humanitarian Report Generator")

# pydantic model
class QueryRequest(BaseModel):
    question: str
    
class QueryResponse(BaseModel):
    answer: str
    

@app.post("/question",  response_model=QueryResponse)
def get_report(request: QueryRequest, credentials: HTTPBasicCredentials = Depends(security)):
    
    if not secrets.compare_digest(credentials.username, correct_username) or \
        not secrets.compare_digest(credentials.password, correct_password):
            raise HTTPException(status_code=401, detail = "Invalid credentials")
    
    try:
        final_report = aga.invoke({"question": request.question})
    except anthropic.APIError as ae:
        raise HTTPException(status_code=500, detail=f"Anthropic API error: {ae}")
    except KeyError as ke:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {ke}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
        
    return {"answer": final_report['final_report']}

if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)