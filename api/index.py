from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Batch API on Vercel"}

@app.get("/batches")
async def get_batches():
    return [
        {
            "batchId": "batch001",
            "batchName": "Python Course",
            "discountPrice": 2999,
            "batchThumb": "https://example.com/image.jpg"
        }
    ]

@app.get("/extract/batch_id={batch_id}")
async def get_details(batch_id: str):
    return {
        "batchId": batch_id,
        "topics": [
            {
                "topicName": "Introduction",
                "lectures": [
                    {
                        "videoTitle": "Video 1",
                        "videoLinks": [{"quality": "720p", "url": "https://example.com/video.mp4"}],
                        "pdfLinks": [{"name": "Notes", "url": "https://example.com/notes.pdf"}]
                    }
                ]
            }
        ]
    }

# Vercel requires this
handler = app
