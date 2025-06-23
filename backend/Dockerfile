# Stage 1: build runtime image
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy only necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Stage 2: runtime image
FROM python:3.11-slim
WORKDIR /app

# Copy everything from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/app /app/app

# Environment setup
ENV PYTHONUNBUFFERED=1
ENV FRONTEND_URL="https://stock-price-prediction-system-liart.vercel.app"

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
