from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging

from .models import RerankerModel

app = FastAPI(title="Reranker Service", version="1.0.0")

# 모델 로드 (시작시 한 번만)
reranker = None

@app.on_event("startup")
async def startup_event():
    global reranker
    logging.info("모델 로딩 중...")
    reranker = RerankerModel()
    logging.info("모델 로딩 완료")

class RerankRequest(BaseModel):
    query: str
    documents: List[str]
    top_k: int = 5

class RerankResponse(BaseModel):
    results: List[dict]

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/rerank", response_model=RerankResponse)
async def rerank_documents(request: RerankRequest):
    try:
        if not reranker:
            raise HTTPException(status_code=503, detail="모델이 로드되지 않았습니다")
        
        results = reranker.rerank(
            query=request.query,
            documents=request.documents,
            top_k=request.top_k
        )
        
        formatted_results = [
            {"document": doc, "score": float(score), "rank": idx + 1}
            for idx, (doc, score) in enumerate(results)
        ]
        
        return RerankResponse(results=formatted_results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)