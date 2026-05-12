from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File

import shutil

from backend.crew import run_ftio_analysis

from backend.services.copilot_engine import (
    generate_copilot_response
)

app = FastAPI(
    title="FTIO API",
    description="Fashion Trend & Inventory Optimizer",
    version="1.0.0"
)

# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# ROOT
# -----------------------------------

@app.get("/")
def root():

    return {
        "message": "FTIO Backend Running"
    }

# -----------------------------------
# HEALTH CHECK
# -----------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

# -----------------------------------
# COPILOT CHAT ENDPOINT
# -----------------------------------

@app.post("/chat")

async def chat_with_ftio(
    payload: dict
):

    user_message = payload.get(
        "message",
        ""
    )

    if not user_message:

        return {

            "response":
            "No message provided."
        }

    response = generate_copilot_response(
        user_message
    )

    return {

        "response": response
    }

# -----------------------------------
# ANALYZE
# -----------------------------------

@app.post("/analyze")
def analyze():

    return run_ftio_analysis()

# -----------------------------------
# CSV UPLOAD
# -----------------------------------

@app.post("/upload")
def upload_inventory(
    file: UploadFile = File(...)
):

    save_path = f"backend/data/{file.filename}"

    with open(save_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "status": "uploaded",
        "filename": file.filename
    }

# -----------------------------------
# GET REPORT
# -----------------------------------

@app.get("/report")
def get_report():

    with open(
        "backend/reports/final_report.md",
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()

    return {
        "report": content
    }