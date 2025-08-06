from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np
from typing import List, Tuple

class RerankerModel:
    def __init__(self):
        # 한국어 성능 좋은 경량 모델
        self.model = CrossEncoder('/app/model')
    
    def rerank(self, query: str, documents: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        # 쿼리-문서 페어 생성
        pairs = [[query, doc] for doc in documents]
        
        # 스코어 계산
        scores = self.model.predict(pairs)
        
        # 스코어 순으로 정렬
        doc_score_pairs = list(zip(documents, scores))
        doc_score_pairs.sort(key=lambda x: x[1], reverse=True)
        
        return doc_score_pairs[:top_k]