'''from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
from matcher import load_students, match_student

# Load config and students at startup
try:
    with open("config.json") as f:
        config = json.load(f)
except Exception:
    raise RuntimeError("Missing or invalid config.json")

students = load_students("data/students.json")

app = FastAPI()

class MatchRequest(BaseModel):
    student_id: str
    goal: str
    preferred_study_time: str
    study_type: str
    personality: list

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/match")
def match(req: MatchRequest):
    #input_student = req.dict()
    input_student = req.model_dump()

    matched_id, score, reason = match_student(input_student, students, config)
    print(reason)
    response = {
        "matched_student_id": matched_id,
        "match_score": score,
        "reasoning": reason
    }
    # Ensure JSON-compatible output and status 200
    return JSONResponse(content=jsonable_encoder(response), status_code=200)
---------------------------------------------------------------------------------------
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
from matcher import load_students, match_student

# Load config and students at startup
try:
    with open("config.json") as f:
        config = json.load(f)
except Exception as e:
    raise RuntimeError(f"Missing or invalid config.json: {e}")

try:
    students = load_students("data/students.json")
except Exception as e:
    raise RuntimeError(f"Missing or invalid students.json: {e}")

app = FastAPI()

class MatchRequest(BaseModel):
    student_id: str
    goal: str
    preferred_study_time: str
    study_type: str
    personality: list

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/match")
def match(req: MatchRequest):
    # Use model_dump() for Pydantic v2+
    input_student = req.model_dump()

    try:

        matched_id, score, reason = match_student(input_student, students, config)
        if(not score and not matched_id):
           raise Exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching error: {e}")


    response = {
        "matched_student_id": matched_id,
        "match_score": score,
        "reasoning": reason
    }
    return JSONResponse(content=jsonable_encoder(response), status_code=200)

@app.get("/version")
def version():
    return {
        "version": config.get("version", "unknown"),
        "config": config
    }
'''
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
import os
import logging
from matcher import load_students, match_student

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get absolute paths for config and data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "config.json")
students_path = os.path.join(BASE_DIR, "data", "students.json")

# Load config and students at startup
try:
    with open(config_path) as f:
        config = json.load(f)
    logger.info(f"Loaded config from {config_path}")
except Exception as e:
    logger.error(f"Missing or invalid config.json: {e}")
    raise RuntimeError(f"Missing or invalid config.json: {e}")

try:
    students = load_students(students_path)
    logger.info(f"Loaded {len(students)} students from {students_path}")
except Exception as e:
    logger.error(f"Missing or invalid students.json: {e}")
    raise RuntimeError(f"Missing or invalid students.json: {e}")

app = FastAPI()

class MatchRequest(BaseModel):
    student_id: str
    goal: str
    preferred_study_time: str
    study_type: str
    personality: list

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/match")
def match(req: MatchRequest):
    input_student = req.model_dump()
    logger.info(f"Received match request: {input_student}")

    try:
        matched_id, score, reason = match_student(input_student, students, config)
        logger.info(f"Match result: matched_id={matched_id}, score={score}, reason={reason}")
        print(f"Match result: matched_id={matched_id}, score={score}, reason={reason}", flush=True)
        if not score and not matched_id:
            logger.warning("No suitable match found.")
    except Exception as e:
        logger.error(f"Matching error: {e}")
        raise HTTPException(status_code=500, detail=f"Matching error: {e}")

    response = {
        "matched_student_id": matched_id,
        "match_score": score,
        "reasoning": reason
    }
    return JSONResponse(content=jsonable_encoder(response), status_code=200)

@app.get("/version")
def version():
    return {
        "version": config.get("version", "unknown"),
        "config": config
    }
