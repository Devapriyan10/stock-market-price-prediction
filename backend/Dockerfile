# Stage 1: build runtime image
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app

# Stage 2: final image
FROM python:3.11-slim
WORKDIR /app

# Copy installed packages and app code
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/app /app/app

ENV PYTHONUNBUFFERED=1
ENV FRONTEND_URL="http://localhost:5173"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
