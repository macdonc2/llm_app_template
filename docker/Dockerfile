FROM python:3.11-slim
WORKDIR /app

COPY alembic.ini .
COPY alembic ./alembic

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ ./src
ENV PYTHONPATH=/app/src

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]