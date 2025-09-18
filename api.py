import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from linkedin_demo import LinkedInProfileAnalyzer
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LinkedIn Profile Analyzer API",
    description="API to analyze LinkedIn profiles and generate funny facts",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LinkedInURLs(BaseModel):
    urls: List[str]
    

@app.post("/analyze-profiles")
async def analyze_profiles(linkedin_urls: LinkedInURLs):
    try:
        ai21_api_key = os.getenv("AI21_API_KEY")
        bright_data_token = os.getenv("BRIGHT_DATA_TOKEN") 
        dataset_id = os.getenv("DATASET_ID", "gd_l1viktl72bvl7bjuj0")
        
        if not ai21_api_key:
            raise HTTPException(status_code=500, detail="AI21_API_KEY not configured")
        
        if not bright_data_token:
            raise HTTPException(status_code=500, detail="BRIGHT_DATA_TOKEN not configured")
        
        analyzer = LinkedInProfileAnalyzer(
            ai21_api_key=ai21_api_key,
            bright_data_token=bright_data_token,
            dataset_id=dataset_id
        )
        
        results = analyzer.analyze_profiles(linkedin_urls.urls)
        return results
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)