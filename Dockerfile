# Use a lightweight Python image
FROM python:3.11-slim

# Environment variables to optimize Python in Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Set default timezone (optional, useful for logs)
    TZ=UTC

WORKDIR /app

# Install necessary system dependencies (if any) and clean cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser
COPY . .
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
