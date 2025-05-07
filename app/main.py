# 🔹 app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import query_router

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router.router)

@app.get("/")
def root():
    return {"message": "LittleScienceAI API 서버 실행 중"}
# 🔹 app/routes/query_router.py

from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.services import scholar_api, web_extractor, nlp_processor
from app.agents.query_agent import generate_inferred_paper
from vector_store.vector_db import search_similar_titles

router = APIRouter()

class QueryRequest(BaseModel):
    input_text: str

class InferenceRequest(BaseModel):
    topic: str
    references: list[str]

@router.post("/query")
def handle_query(data: QueryRequest):
    topic = data.input_text

    # 1. 논문 정의 및 의미 추출
    scholar_info = scholar_api.get_scholar_data(topic)
    web_info = web_extractor.extract_web_content(topic)
    summary, issues = nlp_processor.process_meaning(scholar_info + web_info)

    # 2. 유사 논문 검색
    similar = search_similar_titles(topic)

    return {
        "summary": summary,
        "issues": issues,
        "similar_titles": similar
    }

@router.post("/generate-paper")
def generate_paper(data: InferenceRequest):
    paper = generate_inferred_paper(data.topic, data.references)
    return {
        "inferred_paper": paper
    }
