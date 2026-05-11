from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File

import shutil

from backend.crew import run_ftio_analysis

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
# ANALYZE
# -----------------------------------

@app.post("/analyze")
def analyze():

    result = run_ftio_analysis()

    return {
        "status": "success",
        "report": result
    }

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