# Stage 1: builder (install dependencies)
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app ./app

# Stage 2: runtime
FROM python:3.11-slim
WORKDIR /app

# Copy only the installed packages and application code
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/app ./app

# Environment
ENV PYTHONUNBUFFERED=1
ENV FRONTEND_URL="https://stock-price-prediction-system-liart.vercel.app"

# Expose port and run
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
