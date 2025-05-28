# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app/src/fastApi

# Install system dependencies including SuiteSparse
RUN apt-get update && apt-get install -y \
    build-essential \
    libsuitesparse-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code
COPY . .

# Create directories for results and data
RUN mkdir -p results data

# Expose port 8000
EXPOSE 8000

# Instead of a fixed CMD, use ENTRYPOINT to allow override from docker-compose
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 