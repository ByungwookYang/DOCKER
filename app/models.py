from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np
from typing import List, Tuple

class RerankerModel:
    def __init__(self):
        # 로컬 경로의 bge 모델 사용
        self.model = CrossEncoder('/app/model')
    
    def rerank(self, query: str, documents: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        pairs = [[query, doc] for doc in documents]
        scores = self.model.predict(pairs)
        doc_score_pairs = list(zip(documents, scores))
        doc_score_pairs.sort(key=lambda x: x[1], reverse=True)
        return doc_score_pairs[:top_k]
