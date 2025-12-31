# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port for the FastAPI backend (uvicorn)
EXPOSE 8000

# Default command runs uvicorn expecting a FastAPI `app` in `main.py`.
# Adjust if your FastAPI entrypoint differs.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]