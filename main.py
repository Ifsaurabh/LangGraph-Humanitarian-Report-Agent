    

# imports
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
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
demo_username = os.getenv("DEMO_USERNAME")
demo_password = os.getenv("DEMO_PASSWORD")

# App
app = FastAPI(title="Autonomous Humanitarian Report Generator")

# pydantic model
class QueryRequest(BaseModel):
    question: str = Field(min_length= 20, max_length= 500)
    
    
class QueryResponse(BaseModel):
    answer: str
    

@app.post("/question",  response_model=QueryResponse, description="""
Ask questions about India's humanitarian data — get AI-generated structured reports.

**Best results with questions about:**
- Food commodity prices in a specific Indian state
- Poverty and MPI levels by state  
- Food security situation in a specific region
- Price trends for a specific commodity

**Suggested questions to try:**
- "What is the rice price situation in Bihar?"
- "What is the poverty situation in Uttar Pradesh?"
- "What is the food security situation in Maharashtra?"
- "What is the wheat price trend in Punjab?"
- "What is the poverty level in Rajasthan?"

**Note:** Questions must be between 20-500 characters.
""")
def get_report(request: QueryRequest, credentials: HTTPBasicCredentials = Depends(security)):

    if correct_username is None or correct_password is None:
        raise HTTPException(
            status_code=500,
            detail="Server misconfiguration: auth credentials not set"
        )

    valid_pairs = [(correct_username, correct_password)]
    if demo_username and demo_password:
        valid_pairs.append((demo_username, demo_password))

    is_valid = any(
        secrets.compare_digest(credentials.username, u) and secrets.compare_digest(credentials.password, p)
        for u, p in valid_pairs
    )
    if not is_valid:
        raise HTTPException(status_code=401, detail = "Invalid credentials")
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
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