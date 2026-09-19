from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Backend.pipeline import research_pipeline, refine_report, run_search, run_read, run_write, run_score


app = FastAPI(title="Multi-Agent Research API")


# ---- /search ----
class SearchRequest(BaseModel):
    topic: str

class SearchResponse(BaseModel):
    search_result: str

@app.get("/")
def root():
    return {"message": "Welcome to the Multi-Agent Research API. Use the /docs endpoint for API documentation."}

@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    try:
        result = run_search(request.topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return SearchResponse(search_result=result)


# ---- /read ----
class ReadRequest(BaseModel):
    topic: str
    search_result: str

class ReadResponse(BaseModel):
    scraped_result: str

@app.post("/read", response_model=ReadResponse)
def read(request: ReadRequest):
    try:
        result = run_read(request.topic, request.search_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ReadResponse(scraped_result=result)


class WriteRequest(BaseModel):
    topic: str
    search_result: str
    scraped_result: str

class WriteResponse(BaseModel):
    report: str

@app.post("/write", response_model=WriteResponse)
def write(request: WriteRequest):
    try:
        result = run_write(request.topic, request.search_result, request.scraped_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return WriteResponse(report=result)


class ScoreRequest(BaseModel):
    report: str 

class ScoreResponse(BaseModel):
    feedback: str
    score: int | None

@app.post("/score", response_model=ScoreResponse)
def score(request: ScoreRequest):
    try:
        result = run_score(request.report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ScoreResponse(feedback=result["feedback"], score=result["score"])


# ---- /research (poora pipeline ek call mein — doosre clients ke liye) ----
class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    topic: str
    report: str
    feedback: str
    score: int | None

@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    try:
        result = research_pipeline(request.topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ResearchResponse(
        topic=request.topic,
        report=result["report"],
        feedback=result["feedback"],
        score=result["score"]
    )


class RefineRequest(BaseModel):
    report: str
    feedback: str

class RefineResponse(BaseModel):
    refined_report: str

@app.post("/refine", response_model=RefineResponse)
def refine(request: RefineRequest):
    try:
        refined = refine_report(request.report, request.feedback)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return RefineResponse(refined_report=refined)
