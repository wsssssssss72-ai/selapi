from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json

app = FastAPI(title="Batch API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
BATCHES = [
    {
        "batchId": "batch001",
        "batchName": "Python Masterclass",
        "discountPrice": 2999,
        "batchThumb": "https://example.com/image.jpg"
    },
    {
        "batchId": "batch002", 
        "batchName": "Data Science Course",
        "discountPrice": 4999,
        "batchThumb": "https://example.com/image2.jpg"
    }
]

# Routes
@app.get("/")
async def root():
    return {
        "message": "Batch API is running on Vercel",
        "endpoints": {
            "batches": "/batches",
            "batch_details": "/extract/batch_id={id}",
            "health": "/health"
        }
    }

@app.get("/batches")
async def get_all_batches():
    return BATCHES

@app.get("/extract/batch_id={batch_id}")
async def get_batch_details(batch_id: str):
    if batch_id == "batch001":
        return {
            "batchId": "batch001",
            "batchName": "Python Masterclass",
            "topics": [
                {
                    "topicName": "Introduction",
                    "lectures": [
                        {
                            "videoTitle": "Python Basics",
                            "videoLinks": [
                                {"quality": "720p", "url": "https://example.com/video1.mp4"}
                            ],
                            "pdfLinks": [
                                {"name": "Notes", "url": "https://example.com/notes.pdf"}
                            ]
                        }
                    ]
                }
            ]
        }
    raise HTTPException(status_code=404, detail="Batch not found")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Vercel requires this
handler = app
