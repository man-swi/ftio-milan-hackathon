from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import BaseModel

import shutil
import os
import time

from backend.crew import (
    run_ftio_analysis
)

from backend.services.copilot_engine import (
    generate_copilot_response
)

from backend.tools.load_inventory import (
    initialize_inventory
)

from backend.services.database import (
    initialize_database
)

from backend.services.monitoring_engine import (
    monitoring_engine
)

# -----------------------------------
# INITIALIZE DATABASE
# -----------------------------------

initialize_database()

# -----------------------------------
# INITIALIZE INVENTORY CACHE
# -----------------------------------

initialize_inventory()

# -----------------------------------
# FASTAPI APP
# -----------------------------------

# -----------------------------------
# FASTAPI APP
# -----------------------------------

app = FastAPI(
    title="FTIO API",
    version="1.0.0"
)

# -----------------------------------
# STARTUP MONITORING
# -----------------------------------

@app.on_event("startup")
async def startup_monitoring():

    print(
        "Starting FTIO Autonomous Monitoring..."
    )

    monitoring_engine.start_monitoring()

# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

# -----------------------------------
# CHAT REQUEST MODEL
# -----------------------------------

class ChatRequest(BaseModel):

    message: str


# -----------------------------------
# ROOT
# -----------------------------------

@app.get("/")
async def root():

    return {

        "message":
        "FTIO API Running"
    }


# -----------------------------------
# HEALTH CHECK
# -----------------------------------

@app.get("/health")
async def health_check():

    return {

        "status": "healthy",

        "service": "FTIO Backend"
    }


# -----------------------------------
# UPLOAD INVENTORY
# -----------------------------------

@app.post("/upload")
async def upload_inventory(
    file: UploadFile = File(...)
):

    save_path = (
        "backend/data/current_inventory.csv"
    )

    os.makedirs(
        "backend/data",
        exist_ok=True
    )

    with open(
        save_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {

        "message":
        "Inventory uploaded successfully.",

        "file_path":
        save_path
    }


# -----------------------------------
# RUN FTIO ANALYSIS
# -----------------------------------

@app.post("/analyze")
async def analyze_inventory():

    try:

        try:

            results = run_ftio_analysis()

        except Exception as e:

            if "rate_limit" in str(e).lower():

                print("RATE LIMIT HIT — RETRYING")

                time.sleep(15)

                results = run_ftio_analysis()

            else:

                raise e

        return results

    except Exception as error:

        print("ANALYSIS ERROR:")

        print(str(error))

        return {

            "error": str(error)
        }


# -----------------------------------
# FTIO COPILOT CHAT
# -----------------------------------

@app.post("/chat")
async def chat_with_ftio(
    request: ChatRequest
):

    try:

        response = (
            generate_copilot_response(
                request.message
            )
        )

        return {

            "response": response
        }

    except Exception as error:

        print("COPILOT ERROR:")

        print(str(error))

        return {
            "status": "error",

            "error": str(error)
        }