FROM python:3.9-slim

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY app/ ./app/

# 모델 미리 다운로드 (선택사항)
# 모델을 명시적 경로에 저장
RUN python -c "from sentence_transformers import CrossEncoder; model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-2-v2'); model.save('/app/model')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]