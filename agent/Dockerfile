```dockerfile
# Privacy Sentinel AI API Container
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user early for security
RUN useradd --create-home --shell /bin/bash appuser

# Copy requirements first (for Docker layer caching)
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs
RUN mkdir -p /app/tmp

# Set proper permissions
RUN chown -R appuser:appuser /app
RUN chmod +x /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=info

# Volume mount points (for host mounting in development)
VOLUME ["/app/logs", "/app/tmp"]

# Run the application with correct module path
CMD ["uvicorn", "api.summarizer:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
