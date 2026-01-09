# Privacy Sentinel AI - Phase 0 Dockerfile
FROM python:3.11-slim

# Security configuration
RUN addgroup --system privacy-sentinel && \
    adduser --system --group privacy-sentinel

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ libffi-dev libssl-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
RUN chown -R privacy-sentinel:privacy-sentinel /app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
USER privacy-sentinel
CMD ["uvicorn", "web-scanner.main:app", "--host", "0.0.0.0", "--port", "8000"]
