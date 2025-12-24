from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI(
    title="Batch API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class PDFLink(BaseModel):
    name: str
    url: str

class VideoLink(BaseModel):
    quality: str
    url: str

class Lecture(BaseModel):
    videoTitle: str
    videoLinks: List[VideoLink]
    pdfLinks: List[PDFLink]

class Topic(BaseModel):
    topicName: str
    lectures: List[Lecture]

class StudyMaterial(BaseModel):
    topic: str
    pdfs: List[dict]

class BatchDetails(BaseModel):
    batchId: str
    batchName: str
    topics: List[Topic]
    studyMaterial: List[StudyMaterial]

class Batch(BaseModel):
    batchId: str
    batchName: str
    discountPrice: float
    batchThumb: Optional[str] = ""

# In-memory data storage
batches_data = []
batch_details_data = {}

# Load sample data
def load_sample_data():
    global batches_data, batch_details_data
    
    # Sample batch
    batches_data = [
        {
            "batchId": "batch001",
            "batchName": "Python Masterclass 2024",
            "discountPrice": 2999.00,
            "batchThumb": "https://images.unsplash.com/photo-1526379879527-8559ecfcaec5"
        },
        {
            "batchId": "batch002",
            "batchName": "Data Science Complete Course",
            "discountPrice": 4999.00,
            "batchThumb": "https://images.unsplash.com/photo-1551288049-bebda4e38f71"
        }
    ]
    
    # Sample details
    batch_details_data = {
        "batch001": {
            "batchId": "batch001",
            "batchName": "Python Masterclass 2024",
            "topics": [
                {
                    "topicName": "Introduction to Python",
                    "lectures": [
                        {
                            "videoTitle": "Python Basics - Part 1",
                            "videoLinks": [
                                {"quality": "720p", "url": "https://example.com/videos/python-basics-720p.mp4"},
                                {"quality": "480p", "url": "https://example.com/videos/python-basics-480p.mp4"}
                            ],
                            "pdfLinks": [
                                {"name": "Lecture Notes PDF", "url": "https://example.com/pdf/python-notes-1.pdf"},
                                {"name": "Code Examples", "url": "https://example.com/pdf/python-code-1.pdf"}
                            ]
                        },
                        {
                            "videoTitle": "Python Basics - Part 2",
                            "videoLinks": [
                                {"quality": "720p", "url": "https://example.com/videos/python-basics2-720p.mp4"},
                                {"quality": "480p", "url": "https://example.com/videos/python-basics2-480p.mp4"}
                            ],
                            "pdfLinks": [
                                {"name": "Lecture Notes PDF", "url": "https://example.com/pdf/python-notes-2.pdf"}
                            ]
                        }
                    ]
                },
                {
                    "topicName": "Advanced Python",
                    "lectures": [
                        {
                            "videoTitle": "Decorators and Generators",
                            "videoLinks": [
                                {"quality": "720p", "url": "https://example.com/videos/advanced-python-720p.mp4"}
                            ],
                            "pdfLinks": [
                                {"name": "Advanced Concepts", "url": "https://example.com/pdf/advanced-python.pdf"}
                            ]
                        }
                    ]
                }
            ],
            "studyMaterial": [
                {
                    "topic": "Practice Questions",
                    "pdfs": [
                        {"title": "Exercise Set 1", "link": "https://example.com/pdf/exercise-1.pdf"},
                        {"title": "Exercise Set 2", "link": "https://example.com/pdf/exercise-2.pdf"}
                    ]
                },
                {
                    "topic": "Reference Books",
                    "pdfs": [
                        {"title": "Python Cookbook", "link": "https://example.com/pdf/python-cookbook.pdf"}
                    ]
                }
            ]
        },
        "batch002": {
            "batchId": "batch002",
            "batchName": "Data Science Complete Course",
            "topics": [
                {
                    "topicName": "Data Analysis with Pandas",
                    "lectures": [
                        {
                            "videoTitle": "Pandas Introduction",
                            "videoLinks": [
                                {"quality": "720p", "url": "https://example.com/videos/pandas-intro.mp4"}
                            ],
                            "pdfLinks": [
                                {"name": "Pandas Cheatsheet", "url": "https://example.com/pdf/pandas-cheatsheet.pdf"}
                            ]
                        }
                    ]
                }
            ],
            "studyMaterial": []
        }
    }

# Load data on startup
load_sample_data()

# Routes
@app.get("/")
async def root():
    return {
        "message": "Batch API Service",
        "version": "1.0.0",
        "endpoints": {
            "all_batches": "/api/batches",
            "batch_details": "/api/extract/batch_id={batch_id}",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/batches")
async def get_all_batches():
    """Get all available batches"""
    return batches_data

@app.get("/batch/{batch_id}")
async def get_batch(batch_id: str):
    """Get specific batch by ID"""
    for batch in batches_data:
        if batch["batchId"] == batch_id:
            return batch
    raise HTTPException(status_code=404, detail="Batch not found")

@app.get("/extract/batch_id={batch_id}")
async def get_batch_details(batch_id: str):
    """Get detailed batch information"""
    if batch_id in batch_details_data:
        return batch_details_data[batch_id]
    raise HTTPException(status_code=404, detail="Batch details not found")

@app.post("/batches")
async def create_batch(batch: Batch):
    """Create a new batch (admin only)"""
    batches_data.append(batch.dict())
    return {"message": "Batch created successfully", "batch_id": batch.batchId}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}