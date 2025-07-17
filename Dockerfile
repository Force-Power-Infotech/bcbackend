FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    curl \
    gcc \
    postgresql-client \
    libpq-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Set up wait-for-it script
RUN chmod +x /app/scripts/wait-for-it.sh && \
    ln -s /app/scripts/wait-for-it.sh /usr/local/bin/wait-for-it.sh

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Install Tailwind CSS dependencies
RUN npm ci

# Build Tailwind CSS
RUN npm run build:css && npm cache clean --force

# Set permissions and create directories
RUN chmod +x /usr/local/bin/wait-for-it.sh && \
    chmod +x /app/scripts/startup.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application with wait-for-it
CMD ["/bin/sh", "-c", "/wait-for-it.sh db:5432 -- uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
