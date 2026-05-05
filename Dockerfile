FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies including libatomic1 (required by Node.js for Prisma CLI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libatomic1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (required for Prisma CLI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Pre-generate Prisma client during build (takes ~30-60s, only happens once)
# This runs before container startup, so uvicorn starts immediately
RUN prisma generate

EXPOSE 8000

# At startup: run migrations (should be quick), then start Uvicorn
CMD ["sh", "-c", "prisma migrate deploy --skip-generate || true && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
